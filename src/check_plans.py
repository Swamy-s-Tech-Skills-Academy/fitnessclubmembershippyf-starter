#!/usr/bin/env python3
"""Check plans in database"""
from app import app, db, Plan

with app.app_context():
    plans = Plan.query.all()
    print(f"Plans in database: {len(plans)}")
    for plan in plans:
        print(f"- {plan.name}: ${plan.price}")
