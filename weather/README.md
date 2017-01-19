# Azure Machine Learning Tutorial

## Introduction
Azure Machine Learningのチュートリアルです。
このチュートリアルではAzure Machine Learningを利用し、気象庁のデータから天気の予測モデルを作成します。

## Requirement
このチュートリアルでは以下のものを必要とします。

- Microsoft Excelまたはその互換
- Microsoftアカウント
- Webブラウザー
- Python3の実行環境(option)

## Collecting Data
気象庁の過去の気象データをダウンロードできるサイトへと移動します。
[http://www.data.jma.go.jp/gmd/risk/obsdl/index.php](http://www.data.jma.go.jp/gmd/risk/obsdl/index.php)

**地点を選ぶ**から**都道府県・地方を選択**を押し、好きな地点を選択します。今回は東京を選んでみます。
![1](./img/1.png)

**項目を選ぶ**を押します。**データの種類**を**時別**にし、項目を下図のようにチェックします。

![2](./img/2.png)

**期間を選ぶ**から**連続した期間で表示する**を押し、**最近1カ月**ボタンを押して、直近１カ月の日付を選択します。

ここまでできてたら、右側にある**CSVファイルをダウロード**を押します。

![3](./img/3.png)

csvデータをダウンロードすることができました。

余計な行を削除します。
ダウンロードしたCSVをExcelで開き、1,2,3行目と5,6行目を削除します。

![4](./img/4.png)

![5](./img/5.png)

現在のcsvファイルはshift-jis文字コードなのでutf-8に変換します。

メモ帳などを使ってutf-8に変換しましょう。

utf-8に変換できたらデータ作成は完了です。

## Upload Dataset to ML Studio
Azure Machine LearningではML StudioというWebブラウザー上のアプリケーションで機械学習を設計します。

[https://studio.azureml.net/](https://studio.azureml.net/)にアクセスし、右上の**Sign In**を押します。

正しくMicrosoftアカウントでサインインできれば無料のワークスペースが割り当てられます。

![7](./img/7.png)

先ほど作成したデータをアップロードしてみましょう。

左下の**NEW**ボタンを押し、**Data Set** > **From Local File**を押します。

![8](./img/8.png)

Upload a new datasetのダイアログが表示されたら、**ファイルを選択** から先ほどダウンロードしたcsvファイルを選択します。

**SELECT A TYPE FOR THE NEW DATASE**の項目は**Generic CSV File With a header(.csv)**を選択します。

![9](./img/9.png)

できたら右下のチェックボタンをおします。

左下にこのように表示されればデータのアップロードは完了です。

![10](./img/10.png)

## Create Experiment
Azure MLではデータから機械学習、評価までを1つの**Experiment**と呼んでいます。

新しくExperimentを作成しましょう。
左下の**NEW**ボタンを押し、**Blank Experiment**を選択します。

**Experiment**から**Blank Experiment**を押します。

![11](./img/11.png)

先ほどアップロードしたデータセットをキャンバスへと配置します。

左の項目から**Saved Datasets** > **My Datasetes** > **data.csv**を選択し、キャンバスへとドラッグアンドドロップで配置します。

![12](./img/12.png)

配置したデータセットの下を右クリックし、**Visualize**を押してみましょう。

![15](./img/15.png)

このように各カラムのデータの表示や基本統計データ、ヒストグラムなどが簡単に表示されます。

![16](./img/16.png)

続いて左の項目から**Data Transformation** > **Manipulation** の中にある **Select Columns in Dataset**をドラッグアンドドロップでキャンバスへと配置し、先ほど配置したデータセットの下から矢印を引いてつなげます。

![13](./img/13.png)

また、Select Columns in Datasetを選択した状態で右のペインにある**Launch Column selector**を押します。

![14](./img/14.png)

ここではどのカラムのデータを使うのか、カラムデータの選定を行うことができます。

左のボックスに入っているのが現在のカラムで残したいカラムを右のボックスに入れます。

今回、後ろに(2)などがついているカラムは余計なデータなので省き

- 気温
- 日射時間
- 現地気圧
- 降水量
- 日射量
- 相対湿度

の6つを残します。

![17](./img/17.png)

できたら右下のチェックボタンを押します。

続いてデータを**学習用**と**テスト用**に**分割します**
なぜデータを2つに分割するかというと、学習に使わないデータも残しておかないと、学習したモデルがどれぐらい未知のデータに適用できるか判断できないためです。

学習に使っていない**テスト用データ**に対し、学習モデルが完璧に予測できたら、学習モデルは十分未知データに適用できると言えます。

左の項目から**Data Transformation** > **Sample and Split** > **Split Data**を選択し、キャンバスにドラッグアンドドロップし、Select Columns in Datasetとつなぎます。

![18](./img/18.png)

配置した**Split Data**を選択し、右のペインから**Random of rows in the first output dataset**の項目の中身を**0.7**にします。

ここの数字は、どのくらいのデータを左の出力に流すかという意味です。

今回は7割のデータを左に(学習用)、残りの3割を右側に(テスト用)出力します。

![19](./img/19.png)

続いて学習モデルを作成します。
左の項目から**Machine Learning**>**Train**の中にある**Train Model**を選択します。

![20](./img/20.png)

さらに、学習アルゴリズムを配置します。
今回は**何かの数値データを予測したい**ので**回帰学習(Regression)**をすることになります。

**Machine Learning**>**Initialize Model**>**Regression**の中にある**Neural Network Regression**をキャンバスへドラッグアンドドロップします。

また、下図のようにSplit DataとNeuralNetworkRegressionをTrain Modelへとつなぎます。

![22](./img/22.png)

さらに、**Train Model**を選択し、右のペインから**Launch Column Selector**を押します。

![23](./img/23.png)

ここでは**どのデータを予測したいか**を選択します。
今回は**気温**を予測することにしましょう。Select a single columnに**気温℃**を記述します。

![24](./img/24.png)

できたら右下のチェックマークを押します。

続いて学習モデルをテスト用データに適用するために**Score Model**を配置し、下図のようにつなぎます。

![25](./img/25.png)

さらに、テスト結果の評価用に**Machine Learning**>**Evaluate**の中にある**Evaluate Model**をキャンバスへと配置し、下図のようにつなぎます。

![26](./img/26.png)

## Running Machine Learning

ここまでできたら下にあるRUNボタンを押します。

![27](./img/27.png)

機械学習が実行されます。右上に**Finished running**と表示されれば実験終了です。

![28](./img/28.png)

どのような結果になっているか見てみましょう。Score Modelの下を右クリックしてVisualizeを押します。

![29](./img/29.png)

**Scored Labels**は機械学習によって予測された値です。
今回予測したいのは**気温**なので、気温と見比べてみると、微妙にずれていますが高い時は高く、低い時は低い値がついていることがわかります。

![30](./img/30.png)

データをエクスポートしたい場合は**Convert to CSV**モジュールを下につなげます。

![31](./img/31.png)

もう一度**RUN**ボタンを押し、実験が終了したら**Download**ボタンを押します。

![32](./img/32.png)

ダウンロードできたCSVはUTF-8なのでメモ帳などでShift-JISに変換し、Excelで開き、グラフを書くと下図のようになります。

オレンジが予測結果で青が実際の気温です。
小幅なぶれの気温は対処できていますが大きくぶれている気温は正確に予測できていないことがわかります。

![33](./img/33.png)

## Evaluate Result

ではこの結果はどれぐらい予測精度が正しいのでしょうか。それらを数値で示してくれるものが**Evaluate Model**です。

**Evaluate Model**の下を右クリックして**Visualize**を押します。

![34](./img/34.png)

様々な評価指標が表示されます。この中で一番わかりやすいのが**Mean Absolute Error**です。直訳すると**平均絶対誤差**ですがこれの意味としては、**データセット全体で、平均的にはこれぐらい間違えるよ**ということです。

今回は気温を予測結果にしていましたが、Mean Absolute Errorが2.77ということは、**この予測モデルは平均的に気温を2.77℃間違える精度**ということになります。

まだまだ改善が必要ですね。

![35](./img/35.png)

## Setup WebAPI

さて、この予測モデルを実際にWebサービスとして運用したいとします。

Azure Machine LearningではHttp通信でこの予測モデルを利用できるサービスを非常に簡単に実現することができます。

下にある**Set Up Web Service**を押し、**Predictive Web Service Recommended**を押します。

![36](./img/36.png)

運用用の実験が作成されます。初期は下図のようになっていますが

![37](./img/37.png)

今回はSelect Columnsを通さずに、湿度などのパラメータを入れたら、それを予測モデルに通し、気温の予測結果を出力してくれる実験を作ります。

ですので下図のような形になります。
下図のようにつなぎ変えてください。

![38](./img/38.png)

もう一度**RUN**ボタンを押します。

![39](./img/39.png)

実験が終了したら**Deploy Web Service**ボタンを押します。

![40](./img/40.png)

このような画面になります。**API Key**はリクエスト時のヘッダーに含める情報ですのでどこかにメモしておきます。

**Test**ボタンを押すことでWebサービスのテストをすることができます。

![41](./img/41.png)

テキトーな値を入れてみましょう。

![42](./img/42.png)

予測結果を出力することができました。

![43](./img/43.png)

さらに、**REQUEST/RESPONSE**と書いてあるリンクを押します。

リクエストとレスポンスの仕様が書かれたドキュメントが表示されます。

この通りリクエストを送れば、予測モデルを通した結果をHttpレスポンスで受け取ることができます。

![44](./img/44.png)

一番下までスクロールするとリクエストのサンプルコードがC#とPython、Rで書かれています。
この通りコピペすれば動くので非常に便利です。

![45](./img/45.png)

今回は[test.py](./test.py)にテスト用のpythonスクリプトを置いておきました。urlとapi keyを入れ替えて実行してみると気温予測モデルを通し、気温を出力してくれます。