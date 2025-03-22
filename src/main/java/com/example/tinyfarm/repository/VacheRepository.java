package com.example.tinyfarm.repository;

import  com.example.tinyfarm.entity.Vache;

import org.springframework.data.jpa.repository.JpaRepository;

public interface VacheRepository extends JpaRepository<Vache, String> {
}
