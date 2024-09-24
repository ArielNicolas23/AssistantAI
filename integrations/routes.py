from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from project.models import Integration
from project.integrations.forms import IntegrationForm
from project import db

integration_bp = Blueprint('integration', __name__)

@integration_bp.route('/integration/new', methods=['GET', 'POST'])
@login_required
def new_integration():
    form = IntegrationForm()
    if form.validate_on_submit():
        integration = Integration(
            OwnerID=form.OwnerID.data,
            Type=form.Type.data,
            Token=form.Token.data,
            AssistantID=form.AssistantID.data,
            IsTest=form.IsTest.data
        )
        db.session.add(integration)
        db.session.commit()
        flash('Integration created successfully!', 'success')
        return redirect(url_for('integration.list_integrations'))
    return render_template('new_integration.html', form=form)

@integration_bp.route('/integration/update/<uuid:integration_id>', methods=['GET', 'POST'])
@login_required
def update_integration(integration_id):
    integration = Integration.query.get_or_404(integration_id)
    form = IntegrationForm(obj=integration)
    if form.validate_on_submit():
        integration.Type = form.Type.data
        integration.Token = form.Token.data
        integration.AssistantID = form.AssistantID.data
        integration.IsTest = form.IsTest.data
        db.session.commit()
        flash('Integration updated successfully!', 'success')
        return redirect(url_for('integration.list_integrations'))
    return render_template('update_integration.html', form=form)

@integration_bp.route('/integrations')
@login_required
def list_integrations():
    integrations = Integration.query.all()
    return render_template('list_integrations.html', integrations=integrations)
