from supabase_py import Client
from typing import List

def create_task(supabase: Client, task_name: str) -> int:
    result = supabase.table('tasks').insert({'task_name': task_name}).execute()
    task_id = result['data'][0]['id']
    return task_id

def create_subtasks(supabase: Client, task_id: int, subtasks: List[str]):
    rows = [{'task_id': task_id, 'subtask_name': task, 'is_complete': False} for task in subtasks]
    supabase.table('subtasks').insert(rows).execute()

def update_subtask_completion(supabase: Client, subtask_id: int, is_complete: bool):
    supabase.table('subtasks').update({'is_complete': is_complete}).eq('id', subtask_id).execute()
