//目标- 计划 - 问题 - 方案- 分析

$(document).ready(function () {
    var name = $("input[name='searchName']")[0].value;
    var problemId = $("#proNameId").data("id")


    // console.log("*1*",atrs.length,typeof (atrs),atrs)
    // console.log("*2******:", localStorage.getItem("problemAtt"));
    var atrs = JSON.parse(localStorage.getItem("problemAtt"))
    if (atrs == null) {
        atrs = []
    }
    var atrr = []

    function getAtr() {
        atrr = [];
        let atts = localStorage.getItem("problemAtt")
        let atrs = JSON.parse(atts)
        if (atrs != null) {
            for (let atr = 0; atr < atrs.length; atr++) {
                atrr.push(atrs[atr].id)
            }
        } else {
            atrs = JSON.parse("[]")
        }
        return atrr;
    }

    atrr = getAtr();

    // console.log(atrr)
    $("#prototypeBtn").click(function () {
        var up_Attribute = $("input[name='upAtrr']").data("id")
        var down_Attribute = $("input[name='downAtrr']").data("id")
        var relation = $("input[name='relationAtrr']").data("id")
        var step = $("input[name='stepAtrr']")[0].value
        var name = $("input[name='prototypeName']")[0].value
        // console.log("name:",name,"up_Attribute:",up_Attribute,"down_Attribute:",down_Attribute,"relation:",relation,"step:",step)
        $.get("/createPrototype/", {
            "name": name,
            "up_Attribute": up_Attribute,
            "down_Attribute": down_Attribute,
            "relation": relation,
            "step": step
        }, function (e) {
            alert(e)

        })

    })
    $("#environmentSub").click(function () {

        var prototypeName = $("input[name='prototypeQuest']")[0].value
        var prototypeId = $("input[name='prototypeQuest']").data("id")
        var upName = $("input[name='upQuest']")[0].value
        var upId = $("input[name='upQuest']").data("id")
        var myselfName = $("input[name='myselfQuest']")[0].value
        var myselfId = $("input[name='myselfQuest']").data("id")
        var schemeId = $("#proNameSchemeId").data("id")

        if (prototypeId == "") {
            return alert("请选择原型")
        }
        var checked = 0;//未通过
        if ($("input[name='sect']")[0].checked || $("input[name='sect']")[1].checked) {
            if (!$("input[name='sect']")[0].checked) {
                checked = 1;//通过
            }
        } else {
            return alert("请是否成功")
        }


        $.get("/createEnvironment/", {
            "up_PrototypeName": prototypeName,
            "up_Prototype": prototypeId,

            "up_Attribute_problemName": upName,
            "up_Attribute_problem": upId,

            "down_Attribute_problemName": myselfName,
            "down_Attribute_problem": myselfId,
            "checked": checked,
            "schemeId":schemeId
        }, function (e) {
            alert(e);
        })

    })
    $("#initName").change(function () {
        $("#attrDiv").find("ul").empty()
        $("#attrDiv").attr("style", "display:none;");
    })
    $("#prototypeTbody").on("click", "button[name='suerADD']", function () {
        var m_id = $(this).parent().parent().find("td").eq(0).data("id");
        var m_name = $(this).parent().parent().find("td").eq(1)[0].innerHTML;
        // console.log(m_id,m_name)
        $("input[name='prototypeQuest']").val(m_name);
        $("input[name='prototypeQuest']").data("id", m_id);


    })
    $("#searchPropotype").click(function () {
        var name = $("input[name='searchNamePrototype']")[0].value
        var upName = $("input[name='searchNameUpAttr']")[0].value
        var relationName = $("input[name='searchNameRelationAttr']")[0].value
        var downName = $("input[name='searchNameDownAttr']")[0].value
        console.log("name，", name)
        if (name.trim().length == 0 && upName.trim().length == 0 && relationName.trim().length == 0 && downName.trim().length == 0) {
            alert("输入不能为空")
        } else {
            $.get("/getHadPrototype/", {
                "name": name,
                "upName": upName,
                "relationName": relationName,
                "downName": downName
            }, function (e) {
                $("#prototypeTbody").empty();
                var eJson = JSON.parse(e);
                // alert(eJson.length)
                var xunh = 1
                for (var i in eJson) {
                    var ajson = eJson[i]
                    // console.log("i:",i," pk: ",ajson.pk," r- ",ajson.pk in atrr," y- ",atrr)
                    var butOwri = "<button name='suerADD'>添加</button>"
                    // if (atrr.indexOf(ajson.pk) != -1) {
                    //     butOwrite = "<a style='color:rgb(255,143,16);'>已存在</a>"
                    // }

                    $("#prototypeTbody").append(
                        "<tr>" +
                        "<td data-id='" + ajson.pk + "'>" + xunh + "</td>" +
                        "<td>" + ajson.fields.name + "</td>" +
                        "<td>" + ajson.fields.step + "</td>" +
                        "<td> <input type='submit' data-id=" + ajson.fields.up_Attribute + " value=" + ajson.fields.up_AttributeName + ">" + "</td>" +
                        "<td> <input type='submit' data-id=" + ajson.fields.relation + " value=" + ajson.fields.relationName + ">" + "</td>" +
                        "<td> <input type='submit' data-id=" + ajson.fields.down_Attribute + " value=" + ajson.fields.down_AttributeName + ">" + "</td>" +
                        // "<td ">" + ajson.fields.up_AttributeName + "</td>" +
                        // "<td data-id="+ajson.fields.up_Attribute+">" + ajson.fields.up_AttributeName + "</td>" +
                        "<td>" + butOwri + "</td>" +
                        "</tr>"
                    )

                }
            })
        }

    })
    $("#initBtn").click(function () {
        var name = $("#initName")[0].value
        var description = $("#initDesc")[0].value
        if ($("input[name='initAtrr']")[0].value.length <= 0 || name.trim().length <= 0
            || description.trim().length <= 0) {
            return alert("不能为空")
        }
        var attributeId = {"id": $("input[name='initAtrr']").data("id"), "name": $("input[name='initAtrr']")[0].value}
        // console.log("attributeId",attributeId)
        // console.log("JSONattributeId",attributeId)
        $.get("/createObjInit/", {
            "name": name, "description": description,
            "attributeId": "[" + JSON.stringify(attributeId) + "]"
        }, function (e) {
            // alert(e, typeof(e))
            if (e == "属性已存在") {
                alert(e)
                $.get("/getObjInit/", {"name": name}, function (ea) {

                    $("#attrDiv").attr("style", "display:block;");
                    var eJsona = JSON.parse(ea);
                    $("#attrDiv").find("ul").empty();
                    for (var ia in eJsona) {
                        $("#attrDiv").find("ul").append("<li>" + eJsona[ia].name + "</li>")
                    }
                    return
                })
            } else {
                $("#attrDiv").attr("style", "display:block;");
                var eJson = JSON.parse(e);
                $("#attrDiv").find("ul").empty();
                for (var i in eJson) {
                    $("#attrDiv").find("ul").append("<li>" + eJson[i].name + "</li>")
                }
            }
        })

    })
    $("#attTbody").on("click", "button[name='sureAtt']", function () {
        //    添加上级属性
        var attId = $(this).parent().parent().find("td").eq(0).data("id");
        var attName = $(this).parent().parent().find("td").eq(1)[0].innerHTML;
        $("input[name='upAtrr']").val(attName);
        $("input[name='upAtrr']").data("id", attId);

    })
    $("#relationTbody").on("click", "button[name='sureRe']", function () {
        //    添加关系属性
        var attId = $(this).parent().parent().find("td").eq(0).data("id");
        var attName = $(this).parent().parent().find("td").eq(1)[0].innerHTML;
        $("input[name='relationAtrr']").val(attName);
        $("input[name='relationAtrr']").data("id", attId);

    })

    $("#attTbody").on("click", "button[name='sureAttD']", function () {
        //    添加下级属性
        var attId = $(this).parent().parent().find("td").eq(0).data("id");
        var attName = $(this).parent().parent().find("td").eq(1)[0].innerHTML;
        $("input[name='downAtrr']").val(attName);
        $("input[name='downAtrr']").data("id", attId);

    })
    $("#attTbody").on("click", "button[name='surePrototype']", function () {
        //    添加下级属性
        var attId = $(this).parent().parent().find("td").eq(0).data("id");
        var attName = $(this).parent().parent().find("td").eq(1)[0].innerHTML;
        $("input[name='initAtrr']").val(attName);
        $("input[name='initAtrr']").data("id", attId);

    })


    $("#btnRe").click(function () {
        //  关系
        let reName = $("#reName")[0].value;
        let reDesc = $("#reDesc")[0].value;
        if (reName.trim().length == 0 || reDesc.trim().length < 3) {
            return alert("名称为空 或是 描述过短（3个字)")
        }
        $.get("/createRelation/", {"name": reName, "description": reDesc}, function (e) {
            alert(e)
        })

    })

    $("#btnScheme").click(function () {
        let schemeName = $("#schemeName")[0].value;
        let schemeDesc = $("#schemeDesc")[0].value;
        if (schemeName.trim().length == 0 || schemeDesc.trim().length < 3) {
            return alert("名称为空 或是 描述过短（3个字)")
        }
        $.get("/createAttribute/", {"name": schemeName, "description": schemeDesc}, function (e) {
            alert(e)
        })

    })
    $("#searchRelation").click(function () {
        $("#relationTbody").empty();
        name = $("input[name='searchNameRe']")[0].value;
        $.get("/getRelation/", {"name": name}, function (e) {
            console.log("pppp", e)
            // alert(typeof (e))
            var eJson = JSON.parse(e);
            // alert(eJson.length)
            var xunh = 1
            for (var i in eJson) {
                var ajson = eJson[i]
                // console.log("i:",i," pk: ",ajson.pk," r- ",ajson.pk in atrr," y- ",atrr)
                var butOwrite = "<button name='sureRe'>添加</button>"
                // if (atrr.indexOf(ajson.pk) != -1) {
                //     butOwrite = "<a style='color:rgb(255,143,16);'>已存在</a>"
                // }

                $("#relationTbody").append(
                    "<tr>" +
                    "<td data-id='" + ajson.pk + "'>" + xunh + "</td>" +
                    "<td>" + ajson.fields.name + "</td>" +
                    "<td>" + ajson.fields.description + "</td>" +
                    "<td>" + ajson.fields.relationLv + "</td>" +
                    "<td>" + butOwrite + "</td>" +
                    "</tr>"
                )

                xunh = xunh + 1;

            }
        })
    })
    $("#searchAtt").click(function () {
        $("#attTbody").empty();
        name = $("input[name='searchNameAtt']")[0].value;
        $.get("/getAttribute/", {"name": name}, function (e) {
            console.log("pppp", e)
            // alert(typeof (e))
            var eJson = JSON.parse(e);
            // alert(eJson.length)
            var xunh = 1
            for (var i in eJson) {
                var ajson = eJson[i]
                // console.log("i:",i," pk: ",ajson.pk," r- ",ajson.pk in atrr," y- ",atrr)
                var butOwrite = "<button name='sureAtt'>上级</button>" +
                    "<button name='sureAttD'>下级</button>" +
                    "<button name='surePrototype'>实例</button>"
                // if (atrr.indexOf(ajson.pk) != -1) {
                //     butOwrite = "<a style='color:rgb(255,143,16);'>已存在</a>"
                // }

                $("#attTbody").append(
                    "<tr>" +
                    "<td data-id='" + ajson.pk + "'>" + xunh + "</td>" +
                    "<td>" + ajson.fields.name + "</td>" +
                    "<td>" + ajson.fields.description + "</td>" +
                    "<td>" + ajson.fields.attributeLv + "</td>" +
                    "<td>" + butOwrite + "</td>" +
                    "</tr>"
                )

                xunh = xunh + 1;

            }
        })
    })

    $("#PAsubmit").click(function () {
        // let  name=$(".addPA ").find("input[name='name']").value
        let name = $("input[name='name']")[0].value
        let description = $("input[name='description']")[0].value
        if (name.trim().length == 0 || description.trim().length < 3) {
            return alert("名称为空 或是 描述过短（3个字)")
        }
        $.get('/createAttribute_problem/', {"name": name, "description": description}, function (e) {
            // alert(e)
            $("input[name='name']")[0].value = "";
            $("input[name='description']")[0].value = "";
        })
        // console.log("name:",name)

    })
    $("#searchProblemAtt").click(function () {
        atrr = getAtr();
        name = $("input[name='searchName']")[0].value;
        $("#problemTbody").empty()
        $.get("/getAttribute_problem/", {"name": name}, function (e) {
            // alert(typeof (e))
            // console.log("searchProblemAtt:", e)
            var eJson = JSON.parse(e);
            // alert(eJson.length)
            var xunh = 1


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
        atrr = getAtr();
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
                localStorage.setItem("problemAtt", JSON.stringify(atrs));
                // window.opener.location.reload();

            } else {
                alert(e)
            }
            location.reload()
        })
    })

    $("#problemAttTbody").on("click", "button[name='remove']", function () {
        var attrId = $(this).data("id")
        atrr = getAtr();
        $.get("/analysisPageRemoveAtt/", {"id": problemId, "attrId": attrId}, function (e) {
            // console.log("e；", e);
            for (atr in atrs) {
                // console.log("this atr :" + atr)
                if (e == atrs[atr].id) {
                    atrs.splice(atr, 1)
                }
            }
            ;
            // console.log("****:", atrs)
            localStorage.setItem("problemAtt", JSON.stringify(atrs));
            // console.log("*3******:", localStorage.getItem("problemAtt"));
            window.location.reload();
        })


    })
})