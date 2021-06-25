# 位置と伝承 
場所、日時を指定して見える星座、惑星の名前と高度、方角を伝える。

## 実行するには  
### <実行コード>  
`python3 star_frame_system.py`  

### <動かすために実行するファイル>  
[star_frame_system.py](https://github.com/oshiooshi/Orbit/blob/main/oshio/pos/star_frame_system.py)  

## 学習文を更新するには  
・[star_examples.txt](https://github.com/oshiooshi/Orbit/blob/main/oshio/pos/star_examples.txt)の文章例を更新  
・`python3 star_generate_da_samples.py`を実行（[star_da_sample.dat](https://github.com/oshiooshi/Orbit/blob/main/oshio/pos/star_da_samples.dat)の作成）  
・`python3 star_train_da_model.py`を実行（[star_svc.model](https://github.com/oshiooshi/Orbit/blob/main/oshio/pos/star_svc.model)の作成）  
・`python3 star_generate_concept_samples.py`を実行（[star_concept_samples.dat](https://github.com/oshiooshi/Orbit/blob/main/oshio/pos/star_concept_samples.dat)の作成）  
・`python3 star_train_concept_model.py`を実行（[star_crf.model](https://github.com/oshiooshi/Orbit/blob/main/oshio/pos/star_crf.model)の作成）  
・`python3 star_frame_system.py`の実行で対話スタート   
