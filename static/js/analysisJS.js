//目标- 计划 - 问题 - 方案- 分析

$(document).ready(function () {
    var name = $("input[name='searchName']")[0].value;
    var problemId = $("#proNameId").data("id")
    var atts = localStorage.getItem("problemAtt")

    var atrs = JSON.parse(atts)

    console.log("*1*",atrs.length,typeof (atrs),atrs)
    console.log("*2*",atrs.size)
    // var atrs = JSON.parse(atts)
    var atrr = []
    for (var atr=0;atr<atrs.length;atr++) {

        console.log(atrs[atr])
        atrr.push(atrs[atr].id)
    }
    console.log(atrr)


    $("#searchProblemAtt").click(function () {
        $.get("/getAttribute_problem/", {"name": name}, function (e) {
            // alert(typeof (e))
            console.log(e)
            var eJson = JSON.parse(e);
            // alert(eJson.length)
            var xunh = 1
            $("#problemTbody").empty()
            for (var i in eJson) {
                var ajson = eJson[i]
                // console.log("i:",i," pk: ",ajson.pk," r- ",ajson.pk in atrr," y- ",atrr)
                var butOwrite = "<button name='sure'>确认添加</button>"
                if (atrr.indexOf(ajson.pk) != -1) {
                    butOwrite = "<a style='color:rgb(255,143,16);'>已存在</a>"
                }

                $("#problemTbody").append(
                    "<tr>" +
                    "<td data-id='" + ajson.pk + "'>" + xunh + "</td>" +
                    "<td>" + ajson.fields.name + "</td>" +
                    "<td>" + ajson.fields.description + "</td>" +
                    "<td>" + ajson.fields.Attribute_problem_Lv + "</td>" +
                    "<td>" + butOwrite + "</td>" +
                    "</tr>"
                )

                xunh = xunh + 1;

            }

        })
    })


    $("#problemTbody").on("click", "button[name='sure']", function () {
        //确认添加
        // alert(problemId);
        //属性id

        var id = $(this).parent().parent().find("td:first").data("id")
        var name = $(this).parent().parent().find("td:eq(1)")[0].innerText
        var pj = {"id": id, "name": name, "do": 2}
        // console.log(JSON.stringify(pj))
        var data = {"planStepProblemId": problemId, "problemJson": JSON.stringify(pj)}
        // var data={"problemId":problemId,"problemJson":pj}
        // console.log(name)
        // alert(id)
        $.get("/addPlanStepProblem/", data, function (e) {
            //确认添加
            if (e == "ok") {

                // for (atr in atrs) {
                //     atrr.push(atrs[atr].id)
                // }
                atrs.push(pj)
                localStorage.setItem("problemAtt",atrs)
                // window.opener.location.reload();
                location.reload()
            } else {
                alert(e)
            }

        })
    })

    $("#problemAttTbody").on("click", "button[name='remove']", function () {
        var attrId = $(this).data("id")
        $.get("/analysisPageRemoveAtt/", {"id": problemId, "attrId": attrId}, function (e) {
            console.log("e；", e)
            for (atr in atrs) {
                if (e == atrs[atr].id) {
                    atrs.remove(atrs[atr])
                }
            }
            localStorage.setItem("problemAtt", atrs)
            window.location.reload()
        })


    })
})