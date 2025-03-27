package com.example.tinyfarm.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import  com.example.tinyfarm.entity.Ferme;

import java.util.Optional;

public interface FermeRepository extends JpaRepository<Ferme, Long> {
    Optional<Ferme> findByComptePseudo(String pseudo);
}
