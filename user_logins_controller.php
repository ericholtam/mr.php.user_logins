<?php 

/**
 * user_logins module class
 *
 * @package munkireport
 * @author eholtam
 **/
class User_logins_controller extends Module_controller
{
	
	/*** Protect methods with auth! ****/
	function __construct()
	{
		// Store module path
		$this->module_path = dirname(__FILE__);
	}

	/**
	 * Default method
	 * @author eholtam
	 *
	 **/
	function index()
	{
		echo "You've loaded the user_logins module!";
	}
    
	/**
     * Retrieve data in json format
     *
     **/
     public function get_data($serial_number = '')
     {
        $obj = new View();

        if (! $this->authorized()) {
            $obj->view('json', array('msg' => 'Not authorized'));
            return;
        }

        $queryobj = new user_logins_model;
        $user_logins_tab = array();
        foreach($queryobj->retrieve_records($serial_number) as $shareEntry) {
            $user_logins_tab[] = $shareEntry->rs;
        }

        $obj->view('json', array('msg' => $user_logins_tab));
     }
		
} // END class User_logins_controller
