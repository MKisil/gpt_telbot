import asyncio
import json
import os

from dotenv import find_dotenv, load_dotenv, set_key
from googleapiclient.discovery import build

from openai_client import client

load_dotenv(find_dotenv())


def get_google_sheet_data(api_key, spreadsheet_id):
    def authenticate_sheets(api_key):
        return build('sheets', 'v4', developerKey=api_key).spreadsheets()

    sheets = authenticate_sheets(api_key)

    metadata = sheets.get(spreadsheetId=spreadsheet_id).execute()
    sheets_metadata = metadata.get('sheets', '')
    first_sheet_properties = sheets_metadata[0].get('properties', '')
    range_name = f"Аркуш1!A1:B{first_sheet_properties.get('gridProperties', {}).get('rowCount', 1000)}"

    result = sheets.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])

    return values


def create_jsonl(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for row in data[1:]:
            messages = [
                {"role": "system", "content": data[0][0]},
                {"role": "user", "content": row[0]},
                {"role": "assistant", "content": row[1]}
            ]
            json_obj = {"messages": messages}
            f.write(json.dumps(json_obj, ensure_ascii=False) + '\n')


async def train_model():
    file_path = "training_data.jsonl"
    model_name = "gpt-4o-mini-2024-07-18"
    suffix = "telbot"

    with open(file_path, "rb") as file:
        upload_response = await client.files.create(
            file=file,
            purpose="fine-tune"
        )

    file_id = upload_response.id
    print(f"File uploaded with ID: {file_id}")

    fine_tuning_response = await client.fine_tuning.jobs.create(
        training_file=file_id,
        model=model_name,
        suffix=suffix,
        hyperparameters={
            "n_epochs": 4
        }
    )

    job_id = fine_tuning_response.id
    print(f"Fine-tuning job created with ID: {job_id}")

    while True:
        job_status = await client.fine_tuning.jobs.retrieve(job_id)
        status = job_status.status
        print(f"Fine-tuning job status: {status}")

        if status in ['succeeded', 'failed']:
            break

        await asyncio.sleep(60)

    if status == 'succeeded':
        fine_tuned_model_id = job_status.fine_tuned_model
        print(f"Fine-tuning job completed. Model ID: {fine_tuned_model_id}")

        old_model_id = os.getenv('FINE_TUNED_MODEL_ID')
        if old_model_id:
            await client.models.delete(old_model_id)
            print(f"Old model deleted. Model ID: {old_model_id}")
        set_key(find_dotenv(), 'FINE_TUNED_MODEL_ID', fine_tuned_model_id)
    else:
        print("Fine-tuning job failed.")


if __name__ == '__main__':
    GOOGLE_SPREADSHEET_ID = os.getenv('GOOGLE_SPREADSHEET_ID')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

    data = get_google_sheet_data(GOOGLE_API_KEY, GOOGLE_SPREADSHEET_ID)
    create_jsonl(data, 'training_data.jsonl')
    asyncio.run(train_model())
