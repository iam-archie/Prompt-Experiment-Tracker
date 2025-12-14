from flask import Flask, request, jsonify
from db import SessionLocal, Prompt, Experiment, init_db
from sqlalchemy import select
from datetime import datetime

app = Flask(__name__)
init_db()


def get_session():
    return SessionLocal()


@app.route("/api/prompts", methods=["POST"])
def create_prompt():
    data = request.json or {}
    title = data.get("title")
    prompt_text = data.get("prompt_text")

    if not title or not prompt_text:
        return jsonify({"error": "title and prompt_text are required"}), 400

    session = get_session()
    try:
        p = Prompt(
            title=title,
            task_type=data.get("task_type"),
            tags=data.get("tags"),
            prompt_text=prompt_text,
        )
        session.add(p)
        session.commit()
        session.refresh(p)
        return jsonify({"id": p.id, "message": "Prompt created"}), 201
    finally:
        session.close()


@app.route("/api/prompts", methods=["GET"])
def list_prompts():
    session = get_session()
    try:
        q = session.execute(select(Prompt)).scalars().all()
        items = []
        for p in q:
            items.append({
                "id": p.id,
                "title": p.title,
                "task_type": p.task_type,
                "tags": p.tags,
                "prompt_text": p.prompt_text,
                "created_at": p.created_at.isoformat(),
            })
        return jsonify(items), 200
    finally:
        session.close()


@app.route("/api/experiments", methods=["POST"])
def create_experiment():
    data = request.json or {}
    prompt_id = data.get("prompt_id")
    model_name = data.get("model_name")

    if not prompt_id or not model_name:
        return jsonify({"error": "prompt_id and model_name are required"}), 400

    session = get_session()
    try:
        e = Experiment(
            prompt_id=prompt_id,
            model_name=model_name,
            temperature=data.get("temperature"),
            max_tokens=data.get("max_tokens"),
            rating=data.get("rating"),
            notes=data.get("notes"),
        )
        session.add(e)
        session.commit()
        session.refresh(e)
        return jsonify({"id": e.id, "message": "Experiment logged"}), 201
    finally:
        session.close()


@app.route("/api/experiments", methods=["GET"])
def list_experiments():
    session = get_session()
    try:
        q = session.execute(select(Experiment)).scalars().all()
        items = []
        for e in q:
            items.append({
                "id": e.id,
                "prompt_id": e.prompt_id,
                "model_name": e.model_name,
                "temperature": e.temperature,
                "max_tokens": e.max_tokens,
                "rating": e.rating,
                "notes": e.notes,
                "created_at": e.created_at.isoformat(),
            })
        return jsonify(items), 200
    finally:
        session.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
