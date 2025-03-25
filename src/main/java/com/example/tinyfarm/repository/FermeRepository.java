package com.example.tinyfarm.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import  com.example.tinyfarm.entity.Ferme;

public interface FermeRepository extends JpaRepository<Ferme, String> {
}
