#built-in modules
import subprocess
import json

from typing import Dict, List, Union

#Thirds party module
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel

#Project modules
from constants import (
    AI_MODEL_PATH, 
    GENERATED_RESPONSE_MAX_LENGTH, 
    PALM2_API_KEY_PATH, 
    PALM2_API_URL
)


class TextGenerator:
    def __init__(self) -> None:
        
        # Load the fine-tuned model and tokenizer  
        self.my_chat_model = GPT2LMHeadModel.from_pretrained(AI_MODEL_PATH)
        self.my_chat_tokenizer = GPT2Tokenizer.from_pretrained(AI_MODEL_PATH)
    
    
    def generate_response(self, prompt, max_length=250):
        input_ids = self.my_chat_tokenizer.encode(prompt, return_tensors="pt")

        # Create the attention mask and pad token id
        attention_mask = torch.ones_like(input_ids)
        pad_token_id = self.my_chat_tokenizer.eos_token_id

        output = self.my_chat_model.generate(
            input_ids,
            max_length=max_length,
            num_return_sequences=1,
            attention_mask=attention_mask,
            pad_token_id=pad_token_id
        )
        return self.my_chat_tokenizer.decode(output[0], skip_special_tokens=True)
    
    
    def query(self, query:str) -> (Dict[str, Union[bool, str]]):
        '''
            Generate response to query using language model and return it.
            
            Args:
                query(str): The query to get response for.
            Returns:
                (Dict[str, str | bool]): The response of the query. With properties named success
                with the value true if the responsed has been getted or false if not and the success
                message. 
        '''
        #If time out return time out response. 408
        #If internal error, return error code 500
        #if ressource unavalaible return error code 503
        try:
            response = self.generate_response(query, max_length=GENERATED_RESPONSE_MAX_LENGTH)
            return {
                'success': True, 
                'message':'ok', 
                'response': query,
                'code': 200
            }
        except Exception as error:
            return {
                'success': True, 
                'message': f'Something happend wrong on server {error}', 
                'code': 500
            }
    
    def online_PaLM2(self, query:str) ->Union[List[str], str]:
        '''
            This get a response for a given query using Google PaLM2 Generative ChatBot.
            
            Args:
                query(str): The query to ask response for.
            Returns:
                (str | List[str]): str the error messsage or indication if unable to get
                the response. Else a list of possible reponses.
        '''
        with open(PALM2_API_KEY_PATH, 'r') as file:
            api_key_obj = json.load(file)
            good_url = PALM2_API_URL.format(api_key_obj['apiKey'])
            
            response = subprocess.Popen(
                [
                    'curl', 
                    '-H', 
                    'Content-Type: application/json', 
                    '-d', 
                    '{ "prompt": { "text": "%s"} }'%query, 
                    good_url
                ],
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE)
            out, err = response.communicate() #
            response = json.loads(out.decode('utf8'))
            
            candidates = []
            
            if 'candidates' in response:
                for candidate in response.get('candidates'):
                    candidates.append(candidate['output'])
                return candidates
            else:
                if 'error' in response:
                    return response['error']['message']
                elif 'filters' in response:
                    return '''Unable to give response for unknow reason try again. If the problem persist maybe you did something wrong by given query in bad language or out of context'''
            return 'Unable to give response try agin.'