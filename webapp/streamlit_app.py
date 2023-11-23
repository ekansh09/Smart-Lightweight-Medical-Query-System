import os
import streamlit as st
from med_llama import *

st.set_page_config(layout="wide")
# Design move app further up and remove top padding
st.markdown('''<style>.css-1egvi7u {margin-top: -4rem;}</style>''',
    unsafe_allow_html=True)
# Design change hyperlink href link color
st.markdown('''<style>.css-znku1x a {color: #9d03fc;}</style>''',
    unsafe_allow_html=True)  # darkmode
st.markdown('''<style>.css-znku1x a {color: #9d03fc;}</style>''',
    unsafe_allow_html=True)  # lightmode
# Design change height of text input fields headers
st.markdown('''<style>.css-qrbaxs {min-height: 0.0rem;}</style>''',
    unsafe_allow_html=True)
# Design change spinner color to primary color
st.markdown('''<style>.stSpinner > div > div {border-top-color: #9d03fc;}</style>''',
    unsafe_allow_html=True)
# Design change min height of text input box
st.markdown('''<style>.css-15tx938{min-height: 0.0rem;}</style>''',
    unsafe_allow_html=True)
# Design hide top header line
hide_decoration_bar_style = '''<style>header {visibility: hidden;}</style>'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
# Design hide "made with streamlit" footer menu area
hide_streamlit_footer = """<style>#MainMenu {visibility: hidden;}
                        footer {visibility: hidden;}</style>"""
st.markdown(hide_streamlit_footer, unsafe_allow_html=True)



def llm_generate_1(args):
    model_name = "/scratch/megathon/quant/metaquant"
    ggml_version = "gguf"
    qtype = f"{model_name}.{ggml_version}.{kargs['quant_method']}.bin"
    print(f"Running with quantized model {qtype}")

    !/scratch/megathon/quant/llama.cpp/main -m {qtype} -n {kargs['n']} --repeat_penalty {kargs['penalty']} --color -ngl {kargs['ngl']} -p f"\'{prompt}\'" > output.txt
    with open('output.txt') as f:
        output = f.read()
    os.remove("output.txt")
    return str(output)

def llm_generate_2(args):
    model_name = "/scratch/megathon/quant/metaquant"
    ggml_version = "gguf"
    qtype = f"{model_name}.{ggml_version}.{kargs['quant_method']}.bin"
    print(f"Running with quantized model {qtype}")

    vstore = get_vector_store(kargs, prompt)

    print("Getting context")
    new_prompt = get_context(vstore, prompt)

    !/scratch/megathon/quant/llama.cpp/main -m {qtype} -n {kargs['n']} --repeat_penalty {kargs['penalty']} --color -ngl {kargs['ngl']} -p f"\'{new_prompt}\'" > output.txt
    with open('output.txt') as f:
        output = f.read()
    os.remove("output.txt")
    return str(output)

def main_llm_ans_gen():

    # st.image('img/image_banner.png')  # TITLE and Creator information
    with st.container():
        _,col1,col2,_ = st.columns([6,2,14,1])
        with col1:
            st.image("image/logo.jpeg", width=90)
        with col2:
            st.header(f"Smart Lightweight Medical Query System")

    st.subheader('What is your question? ')
    question = st.text_input(label="question", placeholder="AI")
    with st.expander("SECTION - LLM Input", expanded=True):

        llm_ans1 = ""
        llm_ans2 = ""
        # initialize columns variables
        col1, col2, col3, space, col4 = st.columns([6, 6, 6, 3, 5])
        with col1:
            temp = st.text_input('Temperature', 0.4)
            max_new_tokens = st.text_input('Max. New Tokens', 128)

        with col2:
            acc = st.selectbox('Accelerator',
                               ('GPU', 'CPU'),
                               index=0)
            quant_fact = st.selectbox('Quantization Factor',
                                       ('Q4', 'Q5', 'Vanilla'),
                                       index=2)
        with col3:
            rep_pen = st.text_input("Repetition Penalty", 1.2)
            top_p = st.text_input('Top P', 0.9)

        with col4:
            st.write("\n")  # add spacing
            st.write("\n")  # add spacing
            st.write("\n")  # add spacing
            st.write("\n")  # add spacing
            st.write("\n")  # add spacing

            if st.button('Generate Answer'):
                with st.spinner():

                    input_contents = {}  # let the user input all the datas
                    input_contents["prompt"] = question
                    if (rep_pen is not None):
                        input_contents["penalty"] = rep_pen
                    
                    if (max_new_tokens is not None):
                        input_contents["n"] = max_new_tokens

                    if (acc == "GPU") or (acc == "CPU"):
                        if acc == "GPU":
                            input_contents["device"] = "cuda"
                        else:
                            input_contents["device"] = "cpu"

                    if (quant_fact == 'Q4') or (quant_fact == 'Q5') or (quant_fact == 'Vanilla'):
                        if quant_fact == 'Q4':
                            input_contents["quant_method"] = "q4_k_m"
                        elif quant_fact == 'Q5':
                            input_contents["quant_method"] = "q5_k_m"
                        else:
                            input_contents["quant_method"] = "meta"


                    # if (len(input_contents) == 0):  # remind user to provide data
                    #     st.write('Please fill in some contents for your message!')
                    # if () or (len(input_recipient) == 0):
                    #     st.write('Sender and Recipient names can not be empty!')

                    if (len(input_contents) == 4):  # initiate gpt3 mail gen process
                        llm_ans1 = llm_generate_1(input_contents) #"Hello World"
                        print(llm_ans1)
                        llm_ans2 = llm_generate_2(input_contents)
                        print(llm_ans2)

    if llm_ans1 != "" and llm_ans2 != "":
        st.write('\n')  # add spacing
        st.subheader('\nAnswers!\n')
        with st.expander("", expanded=True):
            col1, space, col2 = st.columns([12, 2, 12])
            with col1:
                st.text_area("Normal LLM:",value=llm_ans1)  #output the results
            with col2:
                st.text_area("Medical LLM:",value=llm_ans2)  #output the results


if __name__ == '__main__':
    # call main function
    main_llm_ans_gen()
