async function generate(){

    let prompt =
        document.getElementById("prompt").value;

    if(prompt.trim()===""){
        alert("請輸入圖片描述");
        return;
    }

    document.getElementById("promptAnalyze").innerHTML="分析中...";
    document.getElementById("pixPrompt").innerHTML="分析中...";
    document.getElementById("imageAnalyze").innerHTML="分析中...";
    document.getElementById("draft").innerHTML="分析中...";
    document.getElementById("suggestions").innerHTML="分析中...";
    document.getElementById("final").innerHTML="分析中...";

    try{

        const response =
        await fetch("/chat",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                message:prompt
            })

        });

        const data =
        await response.json();

        console.log("API回傳:", data);

        if(data.error){

            document.getElementById("final").textContent =
                "錯誤：" + data.error;

            return;
        }

        document.getElementById("promptAnalyze").textContent
            = data.promptAnalyze;

        document.getElementById("pixPrompt").textContent
            = data.pixPrompt;

        document.getElementById("imageAnalyze").textContent
            = data.imageAnalyze;

        document.getElementById("draft").textContent
            = data.draft;

        document.getElementById("suggestions").textContent
            = data.suggestions;

        document.getElementById("final").textContent
            = data.final;
    }

    catch(error){

        console.error(error);

        alert("無法連接 API，請檢查 FastAPI 是否正常啟動。");

    }

}