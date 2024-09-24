from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from project.models import Assistant
from project.assistant.forms import AssistantForm
from project import db

assistant_bp = Blueprint('assistant', __name__)

@assistant_bp.route('/assistant/new', methods=['GET', 'POST'])
@login_required
def new_assistant():
    form = AssistantForm()
    if form.validate_on_submit():
        assistant = Assistant(
            Name=form.Name.data,
            OwnerID=form.OwnerID.data,
            Parameter1=form.Parameter1.data,
            Parameter2=form.Parameter2.data,
            Parameter3=form.Parameter3.data,
            Prompt=form.Prompt.data,
            IsTest=form.IsTest.data
        )
        db.session.add(assistant)
        db.session.commit()
        flash('Assistant created successfully!', 'success')
        return redirect(url_for('assistant.list_assistants'))
    return render_template('new_assistant.html', form=form)

@assistant_bp.route('/assistant/update/<uuid:assistant_id>', methods=['GET', 'POST'])
@login_required
def update_assistant(assistant_id):
    assistant = Assistant.query.get_or_404(assistant_id)
    form = AssistantForm(obj=assistant)
    if form.validate_on_submit():
        assistant.Name = form.Name.data
        assistant.Parameter1 = form.Parameter1.data
        assistant.Parameter2 = form.Parameter2.data
        assistant.Parameter3 = form.Parameter3.data
        assistant.Prompt = form.Prompt.data
        assistant.IsTest = form.IsTest.data
        db.session.commit()
        flash('Assistant updated successfully!', 'success')
        return redirect(url_for('assistant.list_assistants'))
    return render_template('update_assistant.html', form=form)

@assistant_bp.route('/assistants')
@login_required
def list_assistants():
    assistants = Assistant.query.all()
    return render_template('list_assistants.html', assistants=assistants)
