@app.post("/upload_files")
async def upload_files(token: str, file_bytes: bytes, file_name: str):
    token_decrypted = decrypt_token(token)
    if token_decrypted["is_expired"]:
        return {"success": False, "response": "Token expired"}

    username = token_decrypted["token"].split('|')[0]
    bytes_variable = file_bytes

    # insert_query = sqlalchemy.insert(Files).values(Username=username, FileName=file_name, FileContent=file_bytes)
    # files_db_session.execute(insert_query)
    # files_db_session.commit()
    # csv_bytes, file_df = pdf_to_csv_bytes(file_bytes)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(bytes_variable)
        temp_file_path = temp_file.name

    upload_file_object = UploadFile(filename='filename.pdf', file=open(temp_file_path, "rb"))

    # os.remove(temp_file_path)
    file_extension = upload_file_object.filename.split('.').pop()
    file_name = f'client_data_table0.{file_extension}'
    file_name = pdf_file_name_generator(file_name)
    # file_name = token_hex(10)
    file_path = rf"..\file_saver\{file_name}"
    # file_path = rf"C:\Users\Sharon's PC\PycharmProjects\anomaly_detection\file_saver\{file_name}"
    with open(file_path, "wb") as f:
        content = await upload_file_object.read()
        f.write(content)
    return {"success": True, "file_path": file_path, "response": "File Uploaded Successfully!"}