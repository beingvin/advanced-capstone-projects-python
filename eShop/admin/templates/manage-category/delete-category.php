<?php
//include constant file
include('../config/constants.php');

//Check whether ID and image_name value is set or not
if (isset($_GET['id']) and isset($_GET['image_name'])) {

    //1.Get the ID & Image name of the category to be deleted 
    $id = $_GET['id'];
    $image_name = $_GET['image_name'];

    //Remove the pysical image file if available
    if ($image_name != "") {
        $path = "../images/category/" . $image_name;
        //Remove the image
        $remove = unlink($path);
        //If failed to remove image then add error message and stop the process
        if ($remove == false) {

            //Set the session message
            $_SESSION['remove-image'] = "<div class='error'>Failed to remove image.</div>";

            //Redirect to manage category page
            header('location:' . SITE_URL . 'admin/manage-category.php');

            //stop the process 
            die();
        }
    }


    //2.Create query to delete category
    $sql = "DELETE FROM tbl_category WHERE id=$id";

    //3.Execute the query
    $res = mysqli_query($conn, $sql);



    //4.Check whether the query is success or failed
    //5.Redirect to manage category page with message (success/error)
    if ($res == TRUE) {

        //Set the session message
        $_SESSION['delete-category'] = "<div class='success' > Category deleted successfully </div>";

        //Redirect Page to Manage category page 
        header("location:" . SITE_URL . 'admin/manage-category.php');
    } else {


        //Create a Session Variable to Display Message
        $_SESSION['delete-category'] = "<div class='error' >Failed to delete Category </div>";

        //Redirect Page to Manage category page 
        header("location:" . SITE_URL . 'admin/manage-category.php');
    }
} else {

    //Redirect Page to Manage category page 
    header('location:' . SITE_URL . 'admin/manage-category.php');
}