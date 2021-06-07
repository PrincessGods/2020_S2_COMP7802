
<section class="container main mt-5">
    <h2>Create</h2>
    <?php echo validation_errors(); ?>
    <?php echo form_open_multipart("posts/create", array('class' => 'd-flex flex-column'), ""); ?>
        <div class="form-group">
            <label for="inputAddress">Address</label>
            <input type="text" class="form-control" name="address" placeholder="1234 Main St">
        </div>
        <div class="form-group">
            <label for="inputContent">Content</label>
            <textarea type="text" class="form-control" id="contentfield" name="content" placeholder="Apartment, studio, or floor"></textarea>
        </div>
            <div class="form-group">
            <label for="inputTitle">Title</label>
            <input type="text" class="form-control" name="title">
        </div>
        <div class="form-group">
            <label for="inputType">Type</label>
            <select name="type" class="form-control" >
                <option selected>Choose...</option>
                <option>find</option>
                <option>employ</option>
            </select>
        </div>
        <div class="form-group d-flex flex-column">
            <label for="inputImage">Upload Image</label>
            <input type="file" class="" name="userfile" size="20">
        </div>
        <button type="submit" class="btn btn-secondary mt-2 mb-4 ml-auto">Submit</button>
    </form>
</section>