
  <?php
  if ($_POST['code'] == 'PAYMENT_PENDING' || $_POST['code'] == 'PAYMENT_FAILURE')
  // // if (1==2) 
  {
    require_once $_SERVER['DOCUMENT_ROOT'] . '/template/status_head.php';

    $status = "Payment Failed";
    $code = 0;
    $reason = "Your payment is failed due to some reason";
    $url = "https://oxyher.com";
    require_once $_SERVER['DOCUMENT_ROOT'] . '/template/status.php';
    require_once $_SERVER['DOCUMENT_ROOT'] . '/template/status_tail.php';

  } 
  // else if($_POST['code'] == 'PAYMENT_SUCCESS') {
  else if($_POST['code'] == 'PAYMENT_SUCCESS' || $_GET['code'] == "T") {
    require_once $_SERVER['DOCUMENT_ROOT'] . '/template/status_head.php';

    require_once $_SERVER['DOCUMENT_ROOT'] . '/config/functions/make_redirection.php';

    $url = make_the_redirection(12);
    ?>

    <style>
      /* Basic Reset */
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }

      /* Center the content */
      body {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100vh;
        background-color: #f3f4f6;
        font-family: Arial, sans-serif;
        color: #333;
      }

      .container {
        text-align: center;
        max-width: 500px;
        padding: 20px;
      }

      .dot-animation {
        display: flex;
        justify-content: center;
        margin-top: 20px;
      }

      .dot {
        width: 12px;
        height: 12px;
        margin: 0 5px;
        background-color: #4a90e2;
        border-radius: 50%;
        animation: bounce 1.5s infinite;
      }

      .dot:nth-child(1) {
        animation-delay: 0s;
      }

      .dot:nth-child(2) {
        animation-delay: 0.3s;
      }

      .dot:nth-child(3) {
        animation-delay: 0.6s;
      }

      @keyframes bounce {

        0%,
        20%,
        50%,
        80%,
        100% {
          transform: translateY(0);
        }

        40% {
          transform: translateY(-10px);
        }

        60% {
          transform: translateY(-5px);
        }
      }

      .message {
        font-size: 1.2em;
        margin: 10px 0;
        color: #4a4a4a;
      }

      .countdown {
        font-weight: bold;
        color: #4a90e2;
      }
    </style>
    <div class="container">
      <p class="message">Please wait redirecting<span class="dot-animation">
          <span class="dot"></span>
          <span class="dot"></span>
          <span class="dot"></span>
        </span></p>
      <p class="message">Please wait while we take you to the next page in <span id="countdown" class="countdown">5</span>
        seconds.</p>
    </div>

    <script>
      // Countdown Timer and Redirection
      let countdown = 5;
      function updateCountdown() {
        document.getElementById('countdown').textContent = countdown;
        if (countdown > 0) {
         
          countdown--;
        } else {
          window.location.href = "<?php echo $url; ?>";
        }
      }
      setInterval(updateCountdown, 1000);
      </script>
      
      
    <?php
    require_once $_SERVER['DOCUMENT_ROOT'] . '/template/status_tail.php';
  } else {
    header("Content-Type: application/json");
    echo json_encode(["Response" => "Request is invalid"]);
  }
  ?>


