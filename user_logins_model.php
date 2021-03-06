<?php

use CFPropertyList\CFPropertyList;

class User_logins_model extends \Model 
{

	public function __construct($serial='')
	{
		parent::__construct('id', 'user_logins'); //primary key, tablename
		$this->rs['id'] = '';
		$this->rs['serial_number'] = $serial;
		$this->rs['user'] = '';

		$this->serial_number = $serial;
	}
	
	// ------------------------------------------------------------------------
    
	/**
	 * Process data sent by postflight
	 *
	 * @param string data
	 * @author tuxudo
	 **/
	public function process($plist)
	{
		if ( ! $plist){
			throw new Exception("Error Processing Request: No property list found", 1);
		}
		
		$parser = new CFPropertyList();
		$parser->parse($plist, CFPropertyList::FORMAT_XML);
		$myList = array_change_key_case($parser->toArray(), CASE_LOWER);
        		
		$typeList = array(
			'user' => '',
		);
		
		foreach ($myList as $event) {
			foreach ($typeList as $key => $username) {
			    // Keep historical logins so only replace if it already exists
                $this->deleteWhere('serial_number=? AND user=?', array($this->serial_number, $this->user));
                    
                if($this->user != null){ // Make sure there is a username to save
                    $this->id = '';
                    $this->save();
                }

				$this->rs[$key] = $username;

				if(array_key_exists($key, $event))
				{
					$this->rs[$key] = $event[$key];
				}

			}
		// Keep historical logins so only replace if it already exists
		$this->deleteWhere('serial_number=? AND user=?', array($this->serial_number, $this->user));
		$this->id = '';
		$this->save();
		}
	}
}
