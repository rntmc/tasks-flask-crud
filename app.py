from flask import Flask, request,jsonify
from models.task import Task
app = Flask(__name__)

tasks = []
task_id_control = 1 #criada fora para ter um controle, senao toda vez teria o valor de 1.

@app.route("/tasks", methods=["POST"])
def create_task():
  global task_id_control # para utilizar uma variavel que esta fora do metodo
  data = request.get_json()
  new_task = Task(id=task_id_control,title=data["title"], description=data.get("description", "")) # mesma coisa data["title"] = data.get("title")
  task_id_control += 1
  tasks.append(new_task)
  print(tasks)
  return jsonify({"message": "Nova tarefa criada com sucesso"})

@app.route("/tasks", methods=["GET"])
def get_tasks():
  task_list = [task.to_dict() for task in tasks]
  # task_list = []
  # for task in tasks:
  #   task_list.append(task.to_dict())

  output = {
    "tasks": task_list,
    "total_tasks":len(task_list)
  }
  return jsonify(output)

@app.route("/tasks/<int:id>", methods=["GET"])
def get_task(id): # na funcao vai exatamente o mesmo nome do que esta em /<>
  for t in tasks:
    if t.id == id:
      return jsonify(t.to_dict())
  return jsonify({"message": "Nao foi possivel encontrar a atividade."}), 404

@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
  task = None # Pq pode encontrar uma atividade ou nao
  for t in tasks:
    if t.id == id:
      task = t
      break
    
    if task == None:
      return jsonify({"message": "Nao foi possivel encontrar a atividade."}), 404
    
    #novos dados
    data = request.get_json()
    task.title = data['title']
    task.description = data['description']
    task.completed = data['completed']
    print(task)
    return jsonify({"message": "Tarefa atualizada com sucesso"})
  
@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
  task = None 
  for t in tasks:
    print(t)
    if t.id == id:
      task = t
      break # a partir do momento que encontrar a operacao para, nao sera necessario continuar a iterar. melhora performance
      
  if not task:
    return jsonify({"message": "Nao foi possivel encontrar a atividade."}), 404
  
  tasks.remove(task)
  return jsonify({"message": "Tarefa deletada com sucesso."})

if __name__ == "__main__": #servidor local
  app.run(debug=True)