//目标- 计划 -问题
$(document).ready(function () {
    $("#planIn").click(function () {


        var proname = $("#selectlist").data("name")
        // console.log("proname:",proname)
        // alert("proname",proname)
        var planName=$("#selectlist").find("option:selected")[0].innerText;

        var step=$("#selectlist").find("option:selected").data("step")

        // console.log("planName:",planName)


        var planId = $("#selectlist")[0].value

        var searchUrl = encodeURI("/planStepProblemPage/?&planId="
            + planId+"&proname="+proname+"&planName="+planName+"&step="+step);
        window.location.href = searchUrl;


    })


})