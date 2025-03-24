package com.example.tinyfarm.entity;

import java.time.LocalDateTime;

import com.fasterxml.jackson.annotation.JsonBackReference;

import jakarta.persistence.Entity; // représente une date avec heure sans fuseau horaire
import jakarta.persistence.JoinColumn;
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;

import lombok.Data; // Importation de la classe Data de Lombok qui génère automatiquement les méthodes equals, hashCode, toString, getters et setters
@Entity
@Table(name = "vache")
public class Vache {
    private double poids; // Le poids de la vache
    private int age; // L'âge de la vache
    private int qt_lait; // La quantité de lait produite par la vache
    private LocalDateTime dernierRepas;
    private LocalDateTime dernierBreuvage; 
    private LocalDateTime dernierLavage; 
    private LocalDateTime maladeDepuis;

    // la vache connait son propriétaire
    @OneToOne
    @JoinColumn(name = "proprietaire", nullable = false)
    @JsonBackReference
    private Ferme proprietaire; // le propriétaire de la vache

    // Constructeurs
    public Vache() {
        this.poids = 1; // Le poids est initialisé à 1 kg
        this.age = 0; // L'âge est initialisé à 0
        this.qt_lait = 0; // La quantité de lait est initialisée à 0
        
        // Nous considérons que lors de la création de la vache, elle n'est pas nourrie, abreuvée et lavée
        this.dernierRepas = LocalDateTime.now().minusDays(1); // Initialisé à hier 
        this.dernierBreuvage = LocalDateTime.now().minusDays(1); // Initialisé à hier
        this.dernierLavage = LocalDateTime.now().minusDays(1); // Initialisé à hier
        this.maladeDepuis = null; // La vache n'est pas malade
    }
     // Getters et setters si nécessaire (ou utiliser @Data avec Lombok)
}
