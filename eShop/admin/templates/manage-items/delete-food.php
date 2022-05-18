<?php
//include constant file
include('../config/constants.php');

//Check whether ID and image_name value is set or not
if (isset($_GET['id']) and isset($_GET['image_name'])) {
    
    //1.Get the ID & Image name of the food to be deleted 
    $id = $_GET['id'];
    $image_name = $_GET['image_name'];

   //Remove the pysical image file if available
    if ($image_name != "") {

        $path = "../images/food/" . $image_name;
        //Remove the image
        $remove = unlink($path);
        //If failed to remove image then add error message and stop the process
        if ($remove == false) {
            //Set the session message
            $_SESSION['remove-image'] = "<div class='error'>Failed to remove image.</div>";
           
            //Redirect to manage food page
            header('location:' . SITE_URL . 'admin/manage-food.php');

            //stop the process 
            die();
        }
    }


    //2.Create query to delete food 
    $sql = "DELETE FROM tbl_food WHERE id=$id";

    //3.Execute the query
    $res = mysqli_query($conn, $sql);


    //4.Check whether the query is success or failed
    //5.Redirect to manage admin page with message (success/error)
    if ($res == TRUE){

        //Create a Session Variable to Display Message
        $_SESSION['delete-food'] = "<div class='success' > Food deleted successfully </div>";
       
        //Redirect Page to Manage food page
        header("location:" . SITE_URL . 'admin/manage-food.php');
    
    } else {

        // echo 'Failed to delete food';

        //Create a Session Variable to Display Message
        $_SESSION['delete'] = "<div class='error' >Failed to delete food</div>";

        //Redirect Page to Manage food page
        header("location:" . SITE_URL . 'admin/manage-food.php');
    }

} else {
    header('location:' . SITE_URL . 'admin/manage-food.php');
}