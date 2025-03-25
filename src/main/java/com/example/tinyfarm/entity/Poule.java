package com.example.tinyfarm.entity;

import java.time.LocalDateTime; // représente une date avec heure sans fuseau horaire  

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

import lombok.Data; // Importation de la classe Data de Lombok qui génère automatiquement les méthodes equals, hashCode, toString, getters et setters

@Entity
@Table(name = "poule")
@Data
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
    
    // la poule connait son propriétaire
    @ManyToOne
    @JoinColumn(name = "proprietaire", nullable = false)
    private Ferme proprietaire; // le propriétaire des poules

    // Constructeurs

    public Poule() {}


    public Poule(char sexe, double poids, int age) {
        this.poids = poids; // Le poids est initialisé à 0.05 pour le poussin et 2.5 pour la poule et le coq
        this.age = age; // L'âge est initialisé à 0 pour le poussin et 5 pour la poule et le coq
        this.sexe = sexe; // Le sexe est initialisé à 'U' pour le poussin (Unknown), 'F' pour la poule et 'M' pour le coq et 
        this.nbOeuf = 0; // Le nombre d'oeufs est initialisé à 0

        // Nous considérons que lors de la création de la poule, elle n'est pas nourrie, abreuvée et lavée
        this.dernierRepas = LocalDateTime.now().minusDays(1); // Initialisé à hier
        this.dernierBreuvage = LocalDateTime.now().minusDays(1);
        this.dernierLavage = LocalDateTime.now().minusDays(1);        
        this.maladeDepuis = null; // La poule n'est pas malade
    }
    // Getters et setters si nécessaire (ou utiliser @Data avec Lombok)
}