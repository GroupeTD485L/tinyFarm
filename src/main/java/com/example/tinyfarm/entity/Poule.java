package com.example.tinyfarm.entity;

import java.time.LocalDateTime; // représente une date avec heure sans fuseau horaire  

import com.fasterxml.jackson.annotation.JsonBackReference; // Importation de la classe JsonBackReference Cette annotation est utilisée pour gérer les relations bidirectionnelles dans la sérialisation JSON afin d'éviter les boucles infinies

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

// pas utile pour le moment en cas de besoin on l'ajoutera il faudra alors ajouter la dépendance dans le pom.xml
//import lombok.Data; // Importation de la classe Data de Lombok qui génère automatiquement les méthodes equals, hashCode, toString, getters et setters

@Entity
@Table(name = "poule")
public class Poule {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)  // Auto-incrémentation de l'ID
    private Long idPoule; // ID = l'identifiant de la poule
    private double poids; 
    private int age; 
    private char sexe; 
    private int nbOeuf; 
    private LocalDateTime dernierRepas;
    private LocalDateTime dernierBreuvage; 
    private LocalDateTime dernierLavage; 
    private LocalDateTime maladeDepuis;
    
    @ManyToOne
    @JoinColumn(name = "proprietaire", nullable = false)
    @JsonBackReference
    private String proprietaire; // le propriétaire des poules

    // Constructeurs
    public Poule() {}

    public Poule(String proprietaire, char sexe, LocalDateTime dernierRepas, LocalDateTime dernierBreuvage, LocalDateTime dernierLavage) {
        this.poids = 0.05; // Le poids est initialisé à 0.05
        this.age = 0; // L'âge est initialisé à 0
        this.sexe = sexe;
        this.nbOeuf = 0; // Le nombre d'oeufs est initialisé à 0
        this.dernierRepas = dernierRepas;
        this.dernierBreuvage = dernierBreuvage;
        this.dernierLavage = dernierLavage;
        this.maladeDepuis = null; // La poule n'est pas malade
    }
    // Getters et setters si nécessaire (ou utiliser @Data avec Lombok)
}