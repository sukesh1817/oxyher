
<div class="col-lg-8 mx-auto p-4 py-md-5">
    <main>
        <?php if ($code == 1) { ?>
            <h1 class="text-success"><?php echo $status ?></h1>
        <?php } ?>

        <?php if ($code == 0) { ?>
            <h1 class="text-danger"><?php echo $status ?></h1>
        <?php } ?>


        <p class="fs-5 col-md-8"><?php echo $reason ?></p>

        <div class="mb-5">
            <?php if ($code == 1) { ?>
                <a href="<?php echo $url ?>" class="btn btn-dark btn-lg px-4">Redirect please wait...</a>
            <?php } ?>
            <?php if ($code == 0) { ?>
                <a href="<?php echo $url ?>" class="btn btn-dark btn-lg px-4">Go to oxyher</a>
            <?php } ?>

        </div>

        <hr class="col-3 col-md-2 mb-5">

        <div class="row g-5">
            <!-- Quick jump section -->
            <div class="col-md-6">
                <div class="card p-4 mb-4">
                    <div class="card-body">
                        <h2 class="text-body-emphasis">Quick jump</h2>
                        <p>Using the links you can jump quickly to oxyher app.</p>
                        <ul class="list-unstyled ps-0">
                            <li>
                                <a class="icon-link mb-1" href="https://oxyher.com/shop" rel="noopener" target="_blank">
                                    <svg class="bi" width="16" height="16">
                                        <use xlink:href="#arrow-right-circle"></use>
                                    </svg>
                                    Shop
                                </a>
                            </li>
                            <li>
                                <a class="icon-link mb-1" href="https://oxyher.com/shop/cart" rel="noopener"
                                    target="_blank">
                                    <svg class="bi" width="16" height="16">
                                        <use xlink:href="#arrow-right-circle"></use>
                                    </svg>
                                    Cart
                                </a>
                            </li>
                            <li>
                                <a class="icon-link mb-1" href="https://oxyher.com/profile" rel="noopener"
                                    target="_blank">
                                    <svg class="bi" width="16" height="16">
                                        <use xlink:href="#arrow-right-circle"></use>
                                    </svg>
                                    Accounts
                                </a>
                            </li>
                            <li>
                                <a class="icon-link mb-1" href="https://oxyher.com/auth/signin" rel="noopener"
                                    target="_blank">
                                    <svg class="bi" width="16" height="16">
                                        <use xlink:href="#arrow-right-circle"></use>
                                    </svg>
                                    Signin
                                </a>
                            </li>
                            <li>
                                <a class="icon-link mb-1" href="https://oxyher.com/auth/signup" rel="noopener"
                                    target="_blank">
                                    <svg class="bi" width="16" height="16">
                                        <use xlink:href="#arrow-right-circle"></use>
                                    </svg>
                                    Signup
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- Policies section -->
            <div class="col-md-6">
                <div class="card p-4 mb-4">
                    <div class="card-body">
                        <h2 class="text-body-emphasis">Oxyher policies</h2>
                        <p>Read the privacy policies of Oxyher; you must obey to use the app.</p>
                        <ul class="list-unstyled ps-0">
                            <li>
                                <a class="icon-link mb-1" href="https://oxyher.com/agreements/privacy-policy">
                                    <svg class="bi" width="16" height="16">
                                        <use xlink:href="#arrow-right-circle"></use>
                                    </svg>
                                    Privacy policy
                                </a>
                            </li>
                            <li>
                                <a class="icon-link mb-1" href="https://oxyher.com/agreements/return-policy">
                                    <svg class="bi" width="16" height="16">
                                        <use xlink:href="#arrow-right-circle"></use>
                                    </svg>
                                    Refund and cancellation policy
                                </a>
                            </li>
                            <li>
                                <a class="icon-link mb-1" href="https://oxyher.com/agreements/terms-and-conditions">
                                    <svg class="bi" width="16" height="16">
                                        <use xlink:href="#arrow-right-circle"></use>
                                    </svg>
                                    Terms and conditions
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </main>
    <footer class="pt-5 my-5 text-body-secondary border-top">
        Copyright received by Oxyher · © <?php echo date("Y") ?>
    </footer>
</div>