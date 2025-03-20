package com.example.tinyfarm.controller;

import org.springframework.security.core.Authentication;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import com.example.authgithub.service.UserService;

import org.springframework.security.access.prepost.PreAuthorize;


@RestController
@RequestMapping("/counter")
public class CounterController {    

    private final UserService userService;
    public static int count=0;

    public CounterController(UserService userService) {
        this.userService=userService;
    }

    @GetMapping
    @PreAuthorize("isAuthenticated()")
    public int getCounter() {
        return count;
    }

    @PostMapping("/increment")
    @PreAuthorize("isAuthenticated()")
    public void incrementCounter(Authentication authentication) {
        String name=userService.getUsername(authentication);
        System.out.println(name+ " is Incrementing counter");
        count=count+1;
    }
}

