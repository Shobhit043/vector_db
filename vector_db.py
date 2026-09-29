import torch
from transformers import AutoTokenizer, AutoModel
import os
import torch.nn as nn

class vector_db:
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5", model_dir_name: str = 'model') -> None:
        self.model_name = model_name
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        self.model_dir_path = os.path.join(os.getcwd(), model_dir_name)
        os.makedirs(self.model_dir_path, exist_ok=True)

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

        self.model = AutoModel.from_pretrained(model_name, device_map=self.device, cache_dir = self.model_dir_path)
        self.model.eval()

        self.embedd_dim = self.model.get_input_embeddings().embedding_dim
        self.embedds = torch.empty((0, self.embedd_dim))
        self.len = 0
        self.avgdl = 0
        self.docs = []
        self.softmax = nn.Softmax(dim = 1)

    def __len__(self):
        return self.len
    
    def add_doc_list(self, docs: list[str]) -> None:
        if not isinstance(docs, list):
            raise TypeError("docs must a list of string")
        
        if not docs:
            return

        self.docs.extend(docs)
        doc_embedds = []
        for doc in docs:
            doc_embedds.append(self.get_embedd(doc))
            self.len += 1

        self.avgdl = (sum([len(doc.split(" ")) for doc in self.docs])/len(self.docs))
        stacked_doc_embedds = torch.cat(doc_embedds)
        self.embedds = torch.cat((self.embedds, stacked_doc_embedds), dim = 0)
        return self.embedds


    def get_idf_score(self, q: str) -> list[float]:
        idf_scores = []
        N = self.len
        for term in q.split(" "):
            n_q = 0
            for doc in self.docs:
                if term in doc.split(" "):
                    n_q += 1
            idf_scores.append(torch.log(torch.tensor(1+(N - n_q + 0.5)/(n_q + 0.5))).item())
        return idf_scores

    def get_tf_scores(self, q: str, k1: int = 1.2, b: int = 0.75) -> list[float]:
        doc_wise_cnt = []
        for doc in self.docs:
            term_cnts = []
            for qt in q.split(" "):
                cnt = 0
                for term in doc.split(" "):
                    if qt.lower() == term.lower():
                        cnt += 1
                term_cnts.append(cnt)
            doc_wise_cnt.append(term_cnts)

        for i in range(len(doc_wise_cnt)):
            for j in range(len(doc_wise_cnt[i])):
                tf = doc_wise_cnt[i][j]
                doc_wise_cnt[i][j] = (tf*(k1 + 1))/(tf + k1*(1 - b + b*(len(self.docs[i].split(" "))/self.avgdl)))

        return doc_wise_cnt

            

    def get_embedd(self, doc: str) -> torch.Tensor:
        if not isinstance(doc, str):
            raise TypeError("doc must be of string type")
        
        encoded_input = self.tokenizer(doc, padding=True, truncation=True, return_tensors='pt')

        with torch.no_grad():
            model_output = self.model(**encoded_input)
            sentence_embeddings = model_output[0][:, 0]

        sentence_embeddings = torch.nn.functional.normalize(sentence_embeddings, p=2, dim=1)
        return sentence_embeddings


    def similarity_score(self, embd: torch.Tensor) -> torch.Tensor:
        return self.softmax(embd @ self.embedds.T)

    def get_semantic_scores(self, q: str, k: int = 1) -> list[str]:
        qe = self.get_embedd(q)
        scores = self.similarity_score(qe).squeeze(0)
        return scores

    def get_bm25_score(self, q: str) -> list[str]:
        tf_scores = self.get_tf_scores(q)
        idf_scores = self.get_idf_score(q)

        bm25_scores = []
        for i in range(len(tf_scores)):
            score = 0
            for j in range(len(tf_scores[i])):
                score += tf_scores[i][j]*idf_scores[j]
            bm25_scores.append(score)
        return bm25_scores


    def get_ranked_list(self, scores):
        return sorted(range(len(scores)), key = lambda i: scores[i], reverse=True)

    def get_rrf_scores(self, score_lists: list[list[float]], k: int = 60):
        rrf_scores = [0]*len(score_lists[0])
        for ls in score_lists:
            for i in range(len(ls)):
                rrf_scores[ls[i]] += (1 / (k + (i + 1)))
        return rrf_scores
         
    def get_top_k_similar_docs(self, q: str, k: int):
        bm25_ranked_list = self.get_ranked_list(self.get_bm25_score(q))
        semantic_ranked_list = self.get_ranked_list(self.get_semantic_scores(q))
        rrf_ranked_list = self.get_ranked_list(self.get_rrf_scores([bm25_ranked_list, semantic_ranked_list]))
        top_k_docs =  [self.docs[i] for i in rrf_ranked_list[:k]]
        return top_k_docs
        
    
    


    
    