const apiUrl = "http://localhost:8080/api/v1/predict/video"

 function getBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result);
      reader.onerror = error => reject(error);
    });
  }
 async function onUpload() {
    var file = document.querySelector('#files').files[0];
    console.log("getting Base64")
    getBase64(file).then(
        data =>  {
            let myBody = '{"fileName": "' + file.name + '", "fileContent": "' + data + '"}'
            console.log("Body is: " + myBody)
            const userAction = async () => {
                console.log("fetghing_api");
             
                const response = await fetch(apiUrl, {
                  method: 'POST',
                  body: myBody, // string or object
                  headers: {
                    'Content-Type': 'application/json'
                  }
                });
                const emotions = await response.json(); //extract JSON from the http response
                document.querySelector('#mytext').value = JSON.stringify(emotions)
                // do something with myJson
              }
             userAction().then(console.log("called")

             )
        } //
      );


   //filecontent = getBase64(file);
   
 }
