<?php

class Haanga_Extension_Filter_Replaceid
{
    /**
     *  Increment an integer value
     */
    static function main($val, $args)
    {
        return preg_replace("/[x\-]{8,10}/",$args,$val);
    }
}
