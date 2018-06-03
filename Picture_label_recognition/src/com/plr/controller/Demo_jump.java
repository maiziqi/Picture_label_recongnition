package com.plr.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller 
public class Demo_jump {
	@RequestMapping("/demo")
	public String demo() {
		return "demo";
	}
}
