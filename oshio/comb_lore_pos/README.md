# 位置と伝承
### <位置>  
場所、日時を指定して見える星座、惑星の名前と高度、方角を伝える。

### <伝承>  
指定された星座の基本情報と（あれば）伝承を伝える。

## 実行するには  
### <実行コード>  
`python3 comb_frame_system.py`  

### <動かすために実行するファイル>  
[comb_frame_system.py](https://github.com/oshiooshi/Orbit/blob/main/oshio/comb_lore_pos/comb_frame_system.py)  

## 学習文を更新するには  
・[star_examples.txt](https://github.com/oshiooshi/Orbit/blob/main/oshio/comb_lore_pos/star_examples.txt)の文章例を更新  
・`python3 comb_generate_da_samples.py`を実行（[comb_da_sample.dat](https://github.com/oshiooshi/Orbit/blob/main/oshio/comb_lore_pos/comb_da_sample.dat)の作成）  
・`python3 comb_train_da_model.py`を実行（[comb_svc.model](https://github.com/oshiooshi/Orbit/blob/main/oshio/comb_lore_pos/comb_svc.model)の作成）  
・`python3 comb_generate_concept_samples.py`を実行（[comb_concept_samples.dat](https://github.com/oshiooshi/Orbit/blob/main/oshio/comb_lore_pos/comb_concept_samples.dat)の作成）  
・`python3 comb_train_concept_model.py`を実行（[comb_crf.model](https://github.com/oshiooshi/Orbit/blob/main/oshio/comb_lore_pos/comb_crf.model)の作成）  
・`python3 comb_frame_system.py`の実行で対話スタート  
