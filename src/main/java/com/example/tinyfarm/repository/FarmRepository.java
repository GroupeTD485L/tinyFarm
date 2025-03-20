package com.example.tinyfarm.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import  com.example.tinyfarm.entity.Farm;

public interface FarmRepository extends JpaRepository<Farm, String> {
}
