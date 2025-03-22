package com.example.tinyfarm.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import  com.example.tinyfarm.entity.Poule;

public interface PouleRepository extends JpaRepository<Farm, String> {
}
