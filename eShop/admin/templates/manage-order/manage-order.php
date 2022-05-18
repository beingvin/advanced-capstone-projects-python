<?php include('partials/menu.php') ?>


<!-- Main content section starts  -->

<div class="main-content">
    <div class="wrapper">

        <h1>Manage Order</h1> <br>

        <!-- Display session masseges Start-->
        <?php

        if (isset($_SESSION['update-order'])) {

            echo $_SESSION['update-order']; //Displaying Session Message
            unset($_SESSION['update-order']); // removing Session Message

        } elseif (isset($_SESSION['order-not-found'])) {

            echo $_SESSION['order-not-found']; //Displaying Session Message
            unset($_SESSION['order-not-found']); // removing Session Message

        }

        ?>

        <!-- Display session masseges Ends-->

        <br><br>

        <!-- manage orders table -->

        <table class="tbl-full">
            <tr>
                <th>S.N</th>
                <th>Food</th>
                <th>Price</th>
                <th>Qty</th>
                <th>Total</th>
                <th>Order Date</th>
                <th>Status</th>
                <th>Customer Name</th>
                <th>Contact</th>
                <th>Email</th>
                <th>Address</th>
                <th>Actions</th>

            </tr>
            <?php

            //1.sql query to get all order
            $sql = "SELECT * FROM tbl_order ORDER BY id DESC ";

            //2.Execute the query     
            $res = mysqli_query($conn, $sql);

            //3.Check whether query is executed or no 
            if ($res == TRUE) {

                //Count rows to check if we have data in database or not 
                $count = mysqli_num_rows($res); //Function to get all the rows in database 
                $sn = 1; // Create a veriable and assign the value 

                //Check the no of rows 
                if ($count > 0) {

                    //Using while loop to get all the data from database
                    //While loop will run as long as we have data in database
                    while ($row = mysqli_fetch_assoc($res)) {

                        //Get indevidual data 
                        $id = $row['id'];
                        $food = $row['food'];
                        $price = $row['price'];
                        $qty = $row['qty'];
                        $total = $row['total'];
                        $order_date = $row['order_date'];
                        $status = $row['status'];
                        $customer_name = $row['customer_name'];
                        $customer_contact = $row['customer_contact'];
                        $customer_email = $row['customer_email'];
                        $customer_address = $row['customer_address'];

            ?>
            <!-- Display the values in our table  -->
            <tr>
                <td> <?php echo $sn++; ?>. </td>
                <td> <?php echo $food; ?> </td>
                <td> $ <?php echo $price; ?> </td>
                <td> <?php echo $qty; ?> </td>
                <td> <?php echo $total; ?> </td>
                <td> <?php echo $order_date; ?> </td>

                <?php
                            if ($status == "Ordered") {
                            ?>
                <td style="color:blueviolet"> <?php echo $status; ?> </td>
                <?php
                            } elseif ($status == "On Delivery") {
                            ?>
                <td style="color:darkorange"> <?php echo $status; ?> </td>
                <?php
                            } elseif ($status == "Delivered") {
                            ?>
                <td style="color:forestgreen"> <?php echo $status; ?> </td>
                <?php
                            } elseif ($status == "Cancelled") {
                            ?>
                <td style="color:red"> <?php echo $status; ?> </td>
                <?php
                            }

                            ?>

                <td> <?php echo $customer_name; ?> </td>
                <td> <?php echo $customer_contact; ?> </td>
                <td> <?php echo $customer_email; ?> </td>
                <td> <?php echo $customer_address; ?> </td>
                <td>
                    <a href="<?php echo SITE_URL; ?>admin/update-order.php?id=<?php echo $id; ?>"
                        class="secondary-btn">Update Order</a>
                </td>

            </tr>

            <?php

                    }
                }
            }

            ?>

        </table>

    </div>

</div>

<!-- Main content section ends  -->



<!-- Footer section starts  -->

<?php include('partials/footer.php') ?>

<!-- Footer section ends  -->