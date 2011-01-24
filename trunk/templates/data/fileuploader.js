<script type="text/javascript">
dojo.addOnLoad(function(){
    var f0 = new dojox.form.FileUploader({
        //  button: dijit.byId("{{ name }}_btn0"), 
        uploadUrl: "{{ upload_url }}", 
        uploadOnChange: false, 
        selectMultipleFiles: false,
        force: "html",
        fileMask: [],
        isDebug: true,
        devMode: true,
        postData: {sessionid:"TestStuff won't be sent", userId:"DojoMan"}
    }, 'fileuploader_widget');

    doUpload = function(){
        //  dojo.byId("fileToUpload").value = "uploading...";
        f0.upload({postdata:dojo.byId("postdata").value});
    }

    dojo.connect(f0, "onChange", function(dataArray){
        //  console.log("onChange.data:", dataArray);
        dojo.forEach(dataArray, function(d){
            //file.type no workie from flash selection (Mac?)
            dojo.byId("fileToUpload").value = d.name+" "+Math.ceil(d.size*.001)+"kb \n";
        });
    });

    /*
    dojo.connect(f0, "onProgress", function(dataArray){
        console.info("test.onProgress", dataArray);
        dojo.forEach(dataArray, function(d){
            dojo.byId("fileToUpload").value += "onProgress: ("+d.percent+"%) "+d.name+" \n";
            
        });
    });
    */
    dojo.connect(f0, "onComplete", function(dataArray){
        var saved_filename = dataArray[0].uploadedfile;
        console.info("test.onComplete: saved file " + saved_filename);
        dojo.byId('fileuploader_status').innerHTML = 'File uploaded; you may submit the form or upload a different file.';
        dojo.byId('id_{{ name }}').value = saved_filename;
        
        /*
        totalFiles = dataArray.length;
        filesLoaded = 0;
        dojo.forEach(dataArray, function(d){
            dojo.byId("fileToUpload").value += "onComplete: "+d.file+" \n";
            dojo.byId("uploadedFiles").value += "onComplete: "+d.file+" \n";
            dojo.byId("rgtCol").innerHTML += '<img src="'+d.file+'" onload="onFilesLoaded()"/>';
            rmFiles+=d.file+";";
        });
        */
    });

    Destroy = function(){
        f0.destroyAll();
    }
});
</script>