// import React, { Component } from "react";
// import ReactDOM from "react-dom";
// import Indicator from "./indicator/Indicator";

function shortModuleID(moduleID) {
    let blockPattern = /problem\+block@(\w+)/g,
        shortID      = "";
    
    let match = blockPattern.exec(moduleID);

    if (match != null) {
        shortID = match[1];
    }

    return shortID;
}

function dispatchAnswerToGrader(ansobj) {
    let url = `${location.protocol}//${location.host}/courses/${ansobj.course_id}/xblock/${ansobj.problem}/handler/xmodule_handler/problem_check`;
    let dat = {};
    dat[`input_${shortModuleID(ansobj.problem)}_2_1`] = JSON.stringify(ansobj.answer);

    $.ajax({
        type: "POST",
        url: url,
        data: dat,
        success: result => { /* eslint-disable-line no-unused-vars */
            setTimeout(() => { location.reload(); }, 3000);
        },
        error: (request, status, error) => {
            console.error(error);
            console.error(status);
            console.error(request.responseText);
        }
    });
}

// Module IDs for the co-constructed vertical subset
const receiverA = data.receiverA,
      receiverB = data.receiverB;

$(`#problem_${shortModuleID(receiverA)} .problem .action button`).click(e => { /* eslint-disable-line no-unused-vars */
    let handle = runtime.handlerUrl(element, 'problem_submit'),
        ans    = $(`#input_${shortModuleID(receiverA)}_2_1`)[0].value;

    $.ajax({
        type: "POST",
        url: handle,
        data: JSON.stringify({receiver: receiverA, answer: ans}),
        success: dispatchAnswerToGrader
    });
});

$(`#problem_${shortModuleID(receiverB)} .problem .action button`).click(e => { /* eslint-disable-line no-unused-vars */
    let handle = runtime.handlerUrl(element, 'problem_submit'),
        ans    = $(`#input_${shortModuleID(receiverB)}_2_1`)[0].value;

    $.ajax({
        type: "POST",
        url: handle,
        data: JSON.stringify({receiver: receiverB, answer: ans}),
        success: dispatchAnswerToGrader
    });
});
