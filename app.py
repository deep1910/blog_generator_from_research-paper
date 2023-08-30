import streamlit as st
import os
import fitz
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
# from frontend import *
from dotenv import load_dotenv
# import PyPDF2
# import fitz
load_dotenv()

models = {
   
  
    'LLama2-13b-alternative-4k':{
        'USER_ID' : 'clarifai',
        'APP_ID' : 'ml',
# Change these to whatever model and text URL you want to use
        'MODEL_ID' : 'llama2-13b-alternative-4k',
        'MODEL_VERSION_ID' : 'ac68369d73ef4a4a8731e6eafce628ba',
    },

    'GPT-3': {
        'USER_ID': 'openai',
        'APP_ID': 'chat-completion',
        'MODEL_ID': 'GPT-3_5-turbo',
        'MODEL_VERSION_ID': '8ea3880d08a74dc0b39500b99dfaa376'
    },
    'GPT-4': {
        'USER_ID': 'openai',
        'APP_ID': 'chat-completion',
        'MODEL_ID': 'GPT-4',
        'MODEL_VERSION_ID': 'ad16eda6ac054796bf9f348ab6733c72'
    }

}





def extract_text_from_pdf(pdf_path):
   
    
    pdf_document = fitz.open(pdf_path)
    
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text = page.get_text()
        text_Data = [text]
        complete_Data.append(text_Data)
        
         # Adding 1 because page numbers are usually 1-based
        
    pdf_document.close()
    # return None




def prime():
    extract_text_from_pdf(pdf_path)
    
    if complete_Data != 0:
        progress_bar.progress(10)
        st.sidebar.write("The Blog takes some time to generate")

        # st.write("First Step Done")

    

    # j =2 
    chunk = 7
    for i in range(len(complete_Data)):
        # if i+1 < len(complete_Data):
        full_prompt = complete_Data[i][0] + "\n"+   prompt + "\n"
    
        output = format_with_clarifai_api(full_prompt)
    # st.write(output)
        if output != "" :
            pregress = chunk +2
            progress_bar.progress(pregress)
            chunk = chunk + 4
            
            # st.write(f"Page {i+1} Done ")
            complete_output.append(output)
        # st.write(output)
        else:
            st.write(f"Error generating {i} page output.....")
#    


    print(len(complete_output))
    
    # st.write("Step Two Done")
    progress_bar.progress(60)
    
    answer = "".join(complete_output)
    
    progress_bar.progress(80)
    # st.write(answer)
    
    # st.write("Step 3 Done")   

  

    full_answer_prompt = answer + "\n" + blog_prompt + "\n" 
    output_final = format_with_clarifai_api(full_answer_prompt)
    progress_bar.progress(100)
    print(output_final)
# return output_final
    # progress_bar.progress(100)
    # st.write("Output: ")
    # st.write("Your Blog is ready")
    # st.text_area(output_final)
    return output_final





def create_and_upload_file(file_name, data):
    try:
        # Create a new file in the current directory
        with open(file_name, 'w') as file:
            file.write(data)
        print(f"File '{file_name}' created and data uploaded successfully.")
     
        progress_bar.progress(5)

    except Exception as e:
        print(f"An error occurred: {e}")




def extract_text_from_pdf(pdf_path):
   
    
    pdf_document = fitz.open(pdf_path)
    
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text = page.get_text()
        text_Data = [text]
        complete_Data.append(text_Data)
        
         # Adding 1 because page numbers are usually 1-based
        
    pdf_document.close()
    return None






def format_with_clarifai_api( full_prompt):
   


    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    metadata = (('authorization', 'Key ' + PAT),)

    userDataObject = resources_pb2.UserAppIDSet(
        user_id=selected_model['USER_ID'], 
        app_id=selected_model['APP_ID']
    )

    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
            model_id=selected_model['MODEL_ID'],
            version_id=selected_model['MODEL_VERSION_ID'],  # This is optional. Defaults to the latest model version
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                    text=resources_pb2.Text(
                    raw=full_prompt
                    )
                   )
                )
            ]
        ),
        metadata=metadata
    )

    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
       print(post_model_outputs_response.status)
       raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

# Since we have one input, one output will exist here
    output = post_model_outputs_response.outputs[0]
    return output.data.text.raw




def generate_title():
    # full_title_prompt = t + "\n"
    output_title = format_with_clarifai_api(title_complete_prompt)
    print(output_title)
    st.write("Title: ")
    return output_title
    # st.text_area(output_title)
    # return output_title







#msdmpms
























PAT = os.getenv('PAT')
# st.title(PAT)
complete_Data=[]


blog_prompt = "[INST]Write a 500 words interactive blog using real life examples which can be easy to understand using punctuations and emojis where necessary in a human written format[/INST]"
answer = ""
complete_output = []
output_final = ""
prompt = "[INST]extract main data in points[/INST] "
title_prompt = "[INST]Create a attractive SEO friendly title  ,descritption and SEO tags related to  the given blog [/INST] "
output_title = ""





st.set_page_config(page_title="AI BLog Generator!!!" , page_icon=":bar_chart:", layout="wide")
st.title(":bar_chart: AI Blog Generator " )
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)


uploaded_file = st.file_uploader(":file_folder: Upload a file", type=("pdf"))
# if fl is not None:
#     filename = fl.name
#     st.write(filename
# 
if uploaded_file is not None:
   if uploaded_file is not None:
    pdf_bytes = uploaded_file.getvalue()
    with open("temp.pdf", "wb") as temp_pdf:
        temp_pdf.write(pdf_bytes)
        st.write("Saved Successfully")


cwd = os.getcwd()
pdf_path = cwd + "/temp.pdf"




st.sidebar.header("Choose your filter")
selected_model_name= st.sidebar.selectbox("Choose your model", options= list(models.keys()))
selected_model = models[selected_model_name]



    


st.subheader("Your generated Blog")
blog_spot = st.empty()
# blog_spot.text_area("Your generated Blog will be here" , value= )

progress_bar = st.sidebar.empty()
button_clicked = st.sidebar.button("Generate")
if button_clicked:
    output_final = prime()
    blog_spot.text_area("Your BLog is ready!!",height=100, value=output_final, key="blog")
    


st.sidebar.subheader("Generate Title ,description and SEO friendly tags for  the Blog")
title_complete_prompt = output_final+ "\n" +title_prompt +"\n"

title_button_clicked = st.sidebar.button("Generate", key="title_btn")
if title_button_clicked:
  if output_final != None:
     output_title =  generate_title()
  else:
     st.warning("Please Generate Blog first", icon="🚨")     
#   st.text_area(output_title)
# st.text_area("Your Title is ready!!", value=output_title)
# blog_spot.text_area("")
# blog_spot.text_area("Your BLog is ready!!", value=st.session_state.blog,  key="new_blog")
#####START $$$$$$$$$$
title_spot = st.empty()
if output_title != None:
    title_spot.text_area("Output",value=output_title)


