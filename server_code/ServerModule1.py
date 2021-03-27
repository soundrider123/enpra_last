import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
import requests

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
def get_transcription(userid):
  result = requests.get(f'https://43.231.114.140:8080/trans?userid={str(userid)}', verify=False).content.decode("utf-8")
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
  