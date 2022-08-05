from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime
from db import Session
from model import record_table, record_table_temp
from schema import *

import secrets
import os

app = FastAPI()

@app.post('/upload',response_model=ticket,status_code=201)
def upload_link(content_schema:uploadLink):
    '''
    Insert into Database
    '''
    ## Record table
    new_record = record_table()
    new_record.file_address = content_schema.address
    ticket = secrets.token_urlsafe(22)
    new_record.ticket = ticket
    new_record.dt = datetime.now()

    ## Temp record table
    temp_new_record = record_table_temp()
    temp_new_record.file_address = content_schema.address
    temp_new_record.ticket = ticket

    session = Session()

    session.add(new_record)
    session.add(temp_new_record)
    session.commit()
    
    session.close()

    return {'ticket':ticket}

@app.post('/result',response_model=records)
def get_result(content_schema:ticket):
    '''
    Query specific record by the ticket
    '''
    session = Session()

    results = [session.query(record_table).filter(record_table.ticket == content_schema.ticket).first(),]

    session.close()

    if results[0] == None:
        results = []

    returning_schema = records(record_ls = [r.to_dict() for r in results])

    return returning_schema

@app.post('/results',response_model=records)
def get_results(content_schema:tickets):
    '''
    Query records in the database by list of tickets
    '''
    ticket_ls = content_schema.ticket_ls

    session = Session()

    results = session.query(record_table).filter(record_table.ticket.in_(ticket_ls)).all()
    
    session.close()

    returning_schema = records(record_ls = [r.to_dict() for r in results])

    return returning_schema

@app.post('/all_results',response_model=records)
def all_results(content_schema:extraction):
    '''
    Query all records in the database
    '''
    if content_schema.EXTRACT_PW != os.environ['EXTRACT_PW']:
        return JSONResponse(status_code=401,content='EXTRACT_PW not correct')

    session = Session()

    results = session.query(record_table).all()

    session.close()

    returning_schema = records(record_ls = [r.to_dict() for r in results])

    return returning_schema
