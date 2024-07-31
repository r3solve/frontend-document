

def chat_with_data(query:str, chat_history):
    try:
        texts = []
        text_string = ""
        for document in documents:
            file_name = document.filename
            ext = document.filename.split(".")[1]
            text = parser.document_convertor(ext=ext, document=document)
            text_string += f"\nFilename: {file_name}\nContent:\n{text}\n"
            texts.append([{file_name: text}])


        doc_chunk: List[Document] = retriever(doc_text=text_string, query=query)

        text_chunk = ""
        for chunk in doc_chunk:
            text_chunk += chunk.page_content

        #Generate answer to question
        
        #Activate chat session
        activate_session(document=text)

        #Get Chat History



        response = model.extract_info(text=text_chunk, category=category, query=query, chat_history=ai_chat_history)
        

        #suggest followup
        followups = await model.suggest_followups(text=text_chunk, chat_history=ai_chat_history)

        #Update chat history
        await update_chat_history(session_id=session_id, followup_id=followup_id, user_msg=query, ai_response=response)

        return {
            "status": "OK",
            "followups": followups,
            "answer": response
        }
    except sqlite3.Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: str{e}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error processing chat str{e}")