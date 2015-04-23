<?php

class Haanga_Extension_Filter_Increment
{
    /**
     *  Increment an integer value
     */
    static function main($val)
    {
        return ++$val;
    }
}
