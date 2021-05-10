import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
import requests
from io import BytesIO
import pandas as pd
import os

def checkfile(filename1):
  file_exists = False
  if os.path.isfile(f'/{filename1}.csv'):
    file_exists = True
    
  if not file_exists:     
    row = app_tables.csvfile.get(filename=filename1)
    with open(f'/{filename1}.csv', 'w') as f:
      bytes_io = BytesIO(row['filemedia'].get_bytes())
      byte_str = bytes_io.read()
      text_obj = byte_str.decode('UTF-8')
      f.write(text_obj)
      
@anvil.server.callable
def loadtopic():
  
  checkfile('dialog_topic')
  df_topic = pd.read_csv('/dialog_topic.csv', delimiter='|')
  df = df_topic[['topic_id','topic_name']]
  return df.to_dict(orient="records")

@anvil.server.callable
def loadtitle(topic_id):
 
  checkfile('dialog_title')
  checkfile('dialog_dialog')
    
  df = pd.read_csv('/dialog_title.csv', delimiter='|')
  df_dialog1 = pd.read_csv('/dialog_dialog.csv', delimiter='|')
  df_dialog1['topic_id'] = df_dialog1['topic_id'].astype(str)
  df_titleids = df_dialog1[df_dialog1['topic_id'] == str(topic_id)]
  
  title_ids = pd.unique(df_titleids['title_id'])
  
  df = df.loc[df['title_id'].isin(title_ids)]    
    
  return df.to_dict(orient="records")

@anvil.server.callable
def get_title(topic_id):
  
  checkfile('dialog_dialog')
  
  df = pd.read_csv('/dialog_dialog.csv', delimiter='|')
  df['topic_id'] = df['topic_id'].astype(str)
  df = df[df['topic_id'] == str(topic_id)]
  title_id = df['title_id'].min()

  df = pd.read_csv('/dialog_title.csv', delimiter='|')

  df['title_id'] = df['title_id'].astype(str)
  df = df[df['title_id'] == str(title_id)]
  
  return df['title_id'].values[0], df['title_name'].values[0]

@anvil.server.callable
def loaddialog(title_id):
  
  checkfile('dialog_dialog')
    
  df = pd.read_csv('/dialog_dialog.csv', delimiter='|')
  df['title_id'] = df['title_id'].astype(str)
  df = df[df['title_id'] == str(title_id)]
  df = df[['dialog_line']]
  return '\n'.join(df['dialog_line'].values)

@anvil.server.callable
def loadtalk(title_id):
  
  checkfile('dialog_dialog')
    
  df = pd.read_csv('/dialog_dialog.csv', delimiter='|')
  df['title_id'] = df['title_id'].astype(str)
  df = df[df['title_id'] == str(title_id)]
  df = df[['dialog_id', 'dialog_line']]
  return df.to_dict(orient="records")

@anvil.server.callable
def loadanswer(title_id):
  
  checkfile('dialog_dialog')
    
  df = pd.read_csv('/dialog_dialog.csv', delimiter='|')
  df['title_id'] = df['title_id'].astype(str)
  df = df[df['title_id'] == str(title_id)]
  df = df[df['dialog_line'].str.contains('B:')]
   
  df = df[['dialog_id', 'dialog_line']]
  #df = shuffle(df)
  #df = df.reset_index()
  df = df.sample(frac=1).reset_index(drop=True)
  return df.to_dict(orient="records") 

def get_newid():
  max_ids = app_tables.users.search(tables.order_by("userid", ascending=False))
  max_id = 0
  for n in max_ids:
    max_id = int(n['userid'])
    break
  
  max_id = max_id + 1
  return max_id 

@anvil.server.callable
def get_userid():
  username = anvil.google.auth.get_user_email()
  
  user = None
  for u in app_tables.users.search(email = username):
    user = u
  
  if user is None:
    newid = get_newid()
    user = app_tables.users.add_row(email=username, signed_up=datetime.now(), userid=newid)

  for r in app_tables.users.search(email=username):
    userid = r['userid']
    
  return userid

@anvil.server.callable
def get_accuracy(userid, lineid):
  result = requests.get(f'https://43.231.114.140:8080/accuracy?userid={str(userid)}&lineid={str(lineid)}', verify=False).content.decode("utf-8")
  #print(result)
  return result

@anvil.server.callable
def get_transcription(userid,title_id):
  result = requests.get(f'https://43.231.114.140:8080/trans?userid={str(userid)}&titleid={str(title_id)}', verify=False).content.decode("utf-8")
  return result

@anvil.server.callable
def get_htmlcode(userid):
  htmlcode = """

<div>
        <button id="start-recording" >Start Recording</button>
    </div>
    <script type="text/javascript">

    var startRecording = document.getElementById('start-recording');
    var recordAudio;
    
    function get_startrecording_disabled() {       
        return startRecording.disabled;
    } 
      
    function uploadBlob(webmfile) {

        var formData = new FormData();
        formData.append('file', webmfile);
        formData.append('userid', 'loginid');

        $.ajax({
            url: 'https://43.231.114.140:8080/audio',
            data: formData,
            enctype: 'multipart/form-data',
            cache: false,
            contentType: false,
            processData: false,
            type: 'POST',
            success: function (response) {
                console.log(response);
            }
        });

    }      
    
      startRecording.onclick = function() {
        startRecording.disabled = true;
        // make use of HTML 5/WebRTC, JavaScript getUserMedia()
        // to capture the browser microphone stream
        navigator.getUserMedia({
            audio: true
        }, function(stream) {

            recordAudio = RecordRTC(stream, {
                type: 'audio',
                mimeType: 'audio/webm',
                recorderType: StereoAudioRecorder,
                numberOfAudioChannels: 1,
            });

            recordAudio.startRecording();
        }, function(error) {
            console.error(JSON.stringify(error));
        });

        var recordingInterval = setInterval(function () {
            clearInterval(recordingInterval);
            recordAudio.stopRecording(function () {
                var blob = recordAudio.getBlob();
                if (blob.size) { // prevent empty blobs
                    uploadBlob(blob);
                }
            });
            startRecording.disabled = false;
        }, 3000);

    };
      
      
      
    </script>      
    """  
  return htmlcode.replace('loginid', str(userid))
  