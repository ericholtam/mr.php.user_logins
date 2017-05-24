<p>
<table class="user_logins table table-striped table-bordered">
	<thead>
		<tr>
            <th data-i18n="user_logins.user_logins"></th>
		</tr>
	</thead>
	<tbody>
<?php $user_loginsitemobj = new User_logins_model(); ?>
      <?php foreach($user_loginsitemobj->retrieve_records($serial_number) as $item): ?>
        <tr>
          <td><?php echo $item->user; ?></td>
        </tr>
  <?php endforeach; ?>	</tbody>
</table>

<script>
  $(document).on('appReady', function(e, lang) {

        // Initialize datatables
            $('.user_logins').dataTable({
                "bServerSide": false,
                "aaSorting": [[0,'asc']]
            });
  });
</script>
