from flask import jsonify, request,Blueprint
from models import Task,db

task_bp = Blueprint("task_bp",__name__)
@task_bp.route("/tasks")
def fetch_tasks():
    tasks=Task.query.all()
    task_list=[]
    task_list.append({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'completed':task.completed,
        "user": [
            {
                "id": user.id,
                "email": user.email,
                "description": user.password,
            } for user in tasks.user
        ]
    })
    for task in tasks:
        
        return jsonify(task_list)

@task_bp.route("/tasks", methods=['POST'])
def add_tasks():
    data=request.get_json()
    title=data["title"]
    description=data["description"]
    completed=data["completed"]
    user_id=data["user_id"]

    check_title=Task.query.filter_by(title=title).first()
    
    
    if check_title:
        jsonify({"error":"Title exists"}),406
    else:
        new_user=Task(title=title,description=description,completed=completed,user_id=user_id)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"Success":"Added successfully"}),206
    

@task_bp.route("/tasks/<int:task_id>", methods=['PATCH'])
def update_user(task_id):

    task=Task.query.get(task_id)

    if task:
        data=request.get_json()
        title=data.get("title",task.title)
        description=data.get("description",task.description)
        completed=data.get("completed",task.completed)
        user_id=data.get("user_id",task.user.id)

        check_title=Task.query.filter_by(title=title and id != task.id).first()
    
        if check_title:
            jsonify({"error":"Title exists"}),406
        else:
            task.title=title
            task.description=description
            task.completed=completed
            task.user_id=user_id
            
            db.session.commit()
            return jsonify({"Success":"Updated successfully"}),203

    return jsonify({"error":"Task doesn't exist!"}),406

@task_bp.route("/tasks/<int:task_id>", methods=['DELETE'])
def delete_user(task_id):
    task=Task.query.get(task_id)

    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"success":"Deleted successfully"})
    
    else:
        return jsonify({"error":"User being deleted doesn't exist"})
    