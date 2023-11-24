function back()
        {
            var backButton = document.getElementById("backButton");
            var startButton = document.getElementById("startButton");
            var videoFeed = document.getElementById("video_feed");
            var loadingIndicator = document.getElementById("loading_indicator");
            var resultContainer = document.getElementById("result");

            backButton.style.display='none';
            startButton.style.display = "block";
            loadingIndicator.style.display = "none";
            video_feed.style.display='none';

            resultContainer.classList.remove("visible");

            poseClass.style.color='rgba(87, 73, 174, 0.37)';
            poseProb.style.color='rgba(87, 73, 174, 0.37)';

        }
        
        function startCamera() {
            var startButton = document.getElementById("startButton");
            var videoFeed = document.getElementById("video_feed");
            var loadingIndicator = document.getElementById("loading_indicator");
            var resultContainer = document.getElementById("result");
            var resultDiv = document.getElementById("result");
            var poseClassDiv = document.getElementById("poseClass");
            var poseProbDiv = document.getElementById("poseProb");
            var backButton = document.getElementById("backButton")
            
            backButton.style.display = 'block';
            startButton.style.display = "none";
            loadingIndicator.style.display = "block";
           
            // Simulate camera initialization delay
            setTimeout(function() {
                videoFeed.style.display = "block";
                loadingIndicator.style.display = "none";
                resultContainer.classList.add("visible");
            }, 2000); // Change this to the actual time it takes to start the camera

            //Value display
            setTimeout(function() {
                poseClassDiv.style.color='black';
                poseProbDiv.style.color='black';
            }, 2000); 


            // Simulate pose estimation results
            setInterval(function() {
                var body_language_class =  "{{body_language_class}}"; 
                var body_language_prob = "{{body_language_prob}}"; 
                updateResults(resultDiv, body_language_class, body_language_prob);
                updatePoseClass(poseClassDiv, body_language_class); 
                updatePoseProb(poseProbDiv, body_language_prob);
            }, 1000); 
        }

        function updateResults(element, poseClass, poseProbability) {
            element.innerHTML = `<strong>Class:</strong> ${poseClass}<br><strong>Probability:</strong> ${poseProbability.toFixed(2)}`;
        }