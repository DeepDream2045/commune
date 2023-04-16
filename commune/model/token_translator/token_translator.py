import commune
import torch
from typing import Dict, Any, List, Tuple
import streamlit as st
commune.new_event_loop()
from commune.utils.tokenizer import get_translation_map, translate_logits_to_probs_std, \
    translate_special_token_text, pad_offsets, topk_token_phrases, compact_topk_token_phrases, \
        encode_topk, decode_topk

class TokenTranslator(commune.Module):
    def __init__(self, from_tokenizer='facebook/opt-6.7b', to_tokenizer='gpt2'):
        
        self.set_translator(from_tokenizer=from_tokenizer, 
                                to_tokenizer=to_tokenizer)

    def set_translator(self, from_tokenizer, to_tokenizer):
        
        self.from_tokenizer  = self.get_tokenizer(from_tokenizer)
        self.to_tokenizer  = self.get_tokenizer(to_tokenizer)
        self.translation_map= self.get_translation_map(self.from_tokenizer, self.to_tokenizer)
     
        
        
    def translate_logits(self, logits: torch.Tensor):
        
        return logits
    
    def translate_tokens(self, 
                            input_ids:torch.Tensor,
                            return_tensors='pt',
                            padding = True,
                            **kwargs):
        text = self.detokenize(input_ids, tokenizer='from')
        input_ids = self.tokenize(text=text, tokenizer='to' )['input_ids']
        return input_ids
    tokenizer_cache = {}
    def get_tokenizer(cls, tokenizer_name: str, cache:bool = True) -> 'PreTrainedTokenizerBase':
        from transformers import AutoTokenizer
        r"""
        Returns a tokenizer instance for a given tokenizer name.
            Args:
                tokenizer_name (:obj:`str`, `required`):
                    Name of the tokenizer to be loaded.
            Returns:
                tokenizer (:obj:`PreTrainedTokenizerBase`):
                    A tokenizer instance.
        """
        tokenizer = None
        if cache:
            if tokenizer_name in cls.tokenizer_cache:
                tokenizer = cls.tokenizer_cache[tokenizer_name]
            else:
                tokenizer =  AutoTokenizer.from_pretrained(tokenizer_name)

        else:
            tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        
        
        tokenizer = cls.prep_tokenizer(tokenizer)
        
        return tokenizer
    


    @classmethod
    def get_translation_map(cls, from_tokenizer: 'PreTrainedTokenizerBase',
                            to_tokenizer: 'PreTrainedTokenizerBase') -> Dict[str, Any]:
        r"""
        Map individual token phrases from a tokenizer to another tokenizer.
            Args:
                from_tokenizer (:obj:`PreTrainedTokenizerBase`, `required`):
                    From tokenizer.
                to_tokenizer (:obj:`PreTrainedTokenizerBase`, `required`):
                    To tokenizer.

            Returns:
                translation_map (:obj:`Dict[str, Any]`, `required`):
                    Maps for each observed length, a source token to a token sequence of that length,
                    with source index to target indices.
        """

        translation_map = {}

        phrases = from_tokenizer.batch_decode(range(from_tokenizer.vocab_len))  # tokens to strings
        # st.write(phrases[:100])
        to_tokens = to_tokenizer(phrases)['input_ids']  # convert single token from-phrases to to-tokenization
        

            
        translation_map = {}
        counts = {}
        for from_idx, to_idx in enumerate(to_tokens):
            to_idx_len = len(to_idx)
            
            if to_idx_len not in translation_map:
                translation_map[to_idx_len] = {
                    'from': [],
                    'to': []
                }
            
            translation_map[to_idx_len]['from'].append(from_idx)
            translation_map[to_idx_len]['to'].append(to_idx)
            
        for to_idx_len in translation_map.keys():
            for k in ['from', 'to']:
                translation_map[to_idx_len][k] = torch.LongTensor(translation_map[to_idx_len][k])
        
        return translation_map
                


    
    @classmethod
    def set_vocab_len(cls, tokenizer: 'PreTrainedTokenizerBase'):
        r"""
        Sets the tokenizer.vocab_len if unset, to store the real vocabulary size according to the vocab or encoder.
            Args:
                tokenizer (:obj:`PreTrainedTokenizerBase`, `required`):
                    Tokenizer to set vocab_len for.
            Returns:

        """
        if not hasattr(tokenizer, 'vocab_len'):
            if hasattr(tokenizer, 'vocab'):  # use independent vocab_len when tokenizer.vocab_size != len(tokenizer.vocab)
                tokenizer.vocab_len = len(tokenizer.vocab)
            elif hasattr(tokenizer, 'encoder'):  # tokenizers like facebook/opt-* has encoder=vocab
                tokenizer.vocab_len = len(tokenizer.encoder)
            else:  # revert to vocab_size
                tokenizer.vocab_len = tokenizer.vocab_size

    @classmethod
    def prep_tokenizer(cls, tokenizer, std_tokenizer=None):
        tokenizer.padding_side = "left"  # Generative default expects most recent token on right-hand side with padding on left. https://github.com/huggingface/transformers/pull/10552
        # tokenizer.add_prefix_space = False
        # tokenizer.add_special_tokens({'bos_token': "[BOS]"}) # A special token representing the beginning of a sentence.
        # tokenizer.add_special_tokens({'eos_token': "[EOS]"}) # A special token representing the end of a sentence.
        # tokenizer.add_special_tokens({'unk_token': "[UNK]"}) # A special token representing an out-of-vocabulary token.
        # tokenizer.add_special_tokens({'sep_token': "[SEP]"}) # A special token separating two different sentences in the same input (used by BERT for instance)
        # tokenizer.add_special_tokens({'pad_token': "[PAD]"}) # A special token used to make arrays of tokens the same size for batching purpose. Will then be ignored by attention mechanisms or loss computation.
        # tokenizer.add_special_tokens({'cls_token': "[CLS]"}) # A special token representing the class of the input (used by BERT for instance).
        # tokenizer.add_special_tokens({'mask_token': "[MASK]"}) # A special token representing a masked token (used by masked-language modeling pretraining objectives, like BERT).
        # additional_special_tokens = [
        #     "<s>NOTUSED",  # Used by BARThez
        #     "</s>NOTUSED", # Used by BARThez
        #     "<eop>", # Used by MarianMT
        #     "<eod>", # Used by MarianMT
        #     "<formula>", # Used by Transformer XL
        #     "<mask_1>" # Used by Pegasus
        #     "<special0>", # Used by XLM
        #     "<special1>", # Used by XLM
        #     "<special2>", # Used by XLM
        #     "<special3>", # Used by XLM
        #     "<special4>", # Used by XLM
        #     "<special5>", # Used by XLM
        #     "<special6>", # Used by XLM
        #     "<special7>", # Used by XLM
        #     "<special8>", # Used by XLM
        #     "<special9>", # Used by XLM
        # ]
        # tokenizer.additional_special_tokens = additional_special_tokens

        # Define PAD Token = EOS Token (GPT2 generate convention, when PAD Token is None)
        # https://github.com/huggingface/transformers/blob/49c8c67fb815a277405f84dea4a66353e19fb347/tests/models/gpt2/test_modeling_gpt2.py#L532
        if tokenizer.pad_token_id is None and tokenizer.eos_token_id is not None:
            tokenizer.pad_token = tokenizer.eos_token
        cls.set_vocab_len(tokenizer)
        cls.set_whitespace_preserving(tokenizer)

        if std_tokenizer is not None:
            set_std_token_phrases(tokenizer, std_tokenizer)

        return tokenizer
    

    def tokenize(self, 
                 text: str = 'Whadup',
                 padding=True, 
                 truncation=True, 
                 max_length=256,
                 return_tensors='pt',
                 add_special_tokens=False,
                 device:str = None, 
                tokenizer = 'from',
                 **kwargs) -> torch.Tensor:
        """ Returns tokenized text as torch tensor. """
        if tokenizer is None:
            tokenizer = 'from'
        tokenizer = getattr(self, f'{tokenizer}_tokenizer')
        sample = tokenizer(text, 
                                             padding=padding, 
                                             truncation=truncation, 
                                             max_length=max_length, 
                                             return_tensors=return_tensors,
                                             add_special_tokens=add_special_tokens, 
                                             **kwargs)  # assume tokenizer.padding_side = 'left'

        
        sample = dict(
            input_ids= sample['input_ids'],
            attention_mask= sample['attention_mask']
        )
        
        return sample



    def detokenize(self,input_ids: torch.Tensor,
                   tokenizer= 'from', 
                   **kwargs) -> torch.Tensor:
        """ Returns tokenized text as torch tensor. """
        if tokenizer is None:
            tokenizer = 'from'
        tokenizer = getattr(self, f'{tokenizer}_tokenizer')
        text = tokenizer.batch_decode(input_ids,**kwargs)  # assume tokenizer.padding_side = 'left'

        return text



    @staticmethod
    def set_whitespace_preserving(tokenizer: 'PreTrainedTokenizerBase'):
        r"""
        Sets the tokenizer.whitespace_preserving if unset, indicates if tokenizer preserves whitespace like GPT-style,
        or not like BERT-style.
            Args:
                tokenizer (:obj:`PreTrainedTokenizerBase`, `required`):
                    Tokenizer to set vocab_len for.
            Returns:

        """
        if not hasattr(tokenizer, 'whitespace_preserving'):
            space_token = tokenizer(' ', add_special_tokens=False)['input_ids']
            space_text = tokenizer.decode(space_token)
            if space_text == ' ':
                tokenizer.whitespace_preserving = True
            else:
                tokenizer.whitespace_preserving = False

    @classmethod
    def test(cls):
        commune.nest_asyncio()
        cls.print('test')
        
        dataset = commune.connect('dataset.text.bittensor')
        st.write(commune.servers())
        model  = commune.munch({
            'from': commune.connect('model.gpt125m'),
            'to': commune.connect('model.opt6.7b')
            
        })
        
        model_config = { k: m.config for k,m in model.items()}
        tokenizer = { k: m.config['tokenizer'] for k,m in model.items()}

        self = cls(from_tokenizer=tokenizer['from'], to_tokenizer=tokenizer['to'])  

        sample = dataset.sample(no_tokenizer=False)
        # sample = self.from_tokenizer(sample['text'], 
        #                             truncation=True, 
        #                             max_length=64,
        #                             return_tensors='pt',
        #                             add_special_tokens=False,
        #                             padding=True)

        output = model['from'].forward(**sample)
        
        cls.print(output)
        
        output['logits'] = decode_topk(output['topk'], vocab_size=self.from_tokenizer.vocab_len)
        loss_fn = commune.get_module('model.transformer').calculate_loss
        output.update(og_sample)
        loss_fn(**output)
if __name__ == "__main__":
    TokenTranslator.run()
    