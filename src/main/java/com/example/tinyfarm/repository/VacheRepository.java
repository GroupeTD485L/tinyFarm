package com.example.tinyfarm.repository;

import  com.example.tinyfarm.entity.Vache;
import com.example.tinyfarm.entity.Ferme;

import org.springframework.data.jpa.repository.JpaRepository;



public interface VacheRepository extends JpaRepository<Vache, Long> {
    Vache findByProprietaire(Ferme proprietaire);
}
