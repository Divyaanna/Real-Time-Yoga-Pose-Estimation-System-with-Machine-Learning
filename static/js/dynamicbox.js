var socket = io.connect('http://' + document.domain + ':' + location.port);
        
socket.on('update_pose', function(data) {
    var poseClassDiv = document.getElementById("poseClass");
    var poseProbDiv = document.getElementById("poseProb");

    updatePoseClass(poseClassDiv, data.body_language_class);
    updatePoseProb(poseProbDiv, data.body_language_prob);
});
    
function updatePoseClass(element, poseClass) {
    element.innerHTML = `<strong>Current Pose:</strong> ${poseClass}`;
}

function updatePoseProb(element, poseProb) {
    element.innerHTML = `<p><strong>Probability:</strong> ${poseProb}</p>`;
}