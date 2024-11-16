<?php
include_once $_SERVER['DOCUMENT_ROOT'] . '/vendor/autoload.php';

if (isset($_GET['category'])) {
    header("Access-Control-Allow-Origin: *");
    header("Access-Control-Allow-Methods: GET, POST, OPTIONS");
    header("Access-Control-Allow-Headers: Content-Type");

    // Load JSON file for URL configurations
    $jsonFile = '/var/www/api.oxyher.com/config/url/domain.json';
    $jsonData = file_get_contents($jsonFile);
    $url = json_decode($jsonData, true);

    // MongoDB configuration
    $client = new MongoDB\Client("mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.3.1");
    $database = $client->selectDatabase($_GET['category']);
    $collections = $database->listCollections();

    // Price range filter
    $filter = [];
    if (isset($_GET['p_range']) && $_GET['p_range'] != "*") {
        $price = explode("-", $_GET['p_range']);
        if (count($price) === 2) {
            $filter['price'] = [
                '$gte' => (int) $price[0],
                '$lte' => (int) $price[1]
            ];
        }
    }

    // Initialize an array to store all documents
    $all_documents = [];

    // Loop through each collection and fetch documents based on filter
    foreach ($collections as $collection_info) {
        $collection_name = $collection_info->getName();
        $collection = $database->$collection_name;
        $documents = $collection->find($filter)->toArray();

        if (!empty($documents)) {
            $all_documents[$collection_name] = $documents;
        }
    }

    // Check if there are any documents to display
    if (empty($all_documents)) { ?>
        <div class="container d-flex flex-column justify-content-center align-items-center vh-100 text-center">
            <div class="text-muted display-1">
                <i class="fas fa-box-open"></i>
            </div>
            <h2 class="text-danger mt-3">No Products Available</h2>
            <p class="text-dark">We couldn’t find any products within this price range.</p>
            <a href="/shop" class="btn btn-primary mt-3">Return to Shop</a>
        </div>
    <?php } else {
        foreach ($all_documents as $collection_name => $documents) {
            foreach ($documents as $single_item) { ?>

                <div class="col-lg-4 col-md-6 col-sm-12 pb-1">
                    <div class="card product-item border-0 mb-4">
                        <div class="card-header product-img position-relative overflow-hidden bg-transparent border p-0">
                            <a href="<?php echo $url['PRODUCT_URL'] . $single_item['product_id'] ?>">
                                <img class="img-fluid w-100" src="<?php echo $url['IMG_URL'] . $single_item['img_url'][0] ?>" alt="">
                            </a>
                        </div>
                        <div class="card-body border-left border-right text-center p-0 pt-4 pb-3">
                            <h6 class="text-truncate mb-3"><?php echo htmlspecialchars($single_item['title']); ?></h6>
                            <div class="d-flex justify-content-center">
                                <?php if ($single_item['quantity'] > 0) { ?>
                                    <h6><?php echo floatval($single_item['price']); ?> Rs</h6>
                                <?php } else { ?>
                                    <h6 class="text-danger">Out of stock</h6>
                                <?php } ?>
                            </div>
                        </div>
                        <div
                            class="card-footer <?php echo $single_item['quantity'] > 0 ? "d-flex justify-content-between" : ""; ?> bg-light border">
                            <?php if ($single_item['quantity'] > 0) { ?>
                                <a href="<?php echo $url['ADD_CART_URL'] . $single_item['product_id']; ?>" class="btn btn-sm text-dark p-0">
                                    <i class="fas fa-shopping-bag text-primary mr-1"></i>Add to cart
                                </a>
                                <a href="<?php echo $url['ADD_CART_URL'] . $single_item['product_id']; ?>" class="btn btn-sm text-dark p-0">
                                    <i class="fas fa-shopping-cart text-primary mr-1"></i>Buy now
                                </a>
                            <?php } else { ?>
                                <p style="margin:0px;text-align:center;">
                                    <small>Product currently unavailable</small>
                                </p>
                            <?php } ?>
                        </div>
                    </div>
                </div>

            <?php }
        }
    }
}
?>