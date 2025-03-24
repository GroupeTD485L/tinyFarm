package com.example.tinyfarm.entity;
import java.time.LocalDateTime;

import com.fasterxml.jackson.annotation.JsonBackReference;

import jakarta.persistence.Entity; // représente une date avec heure sans fuseau horaire
import jakarta.persistence.JoinColumn;
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;

import lombok.Data; // Importation de la classe Data de Lombok qui génère automatiquement les méthodes equals, hashCode, toString, getters et setters

@Entity
@Table(name = "clapier")
@Data
public class Clapier {
    
    private int nb_bebe;
    private int nb_petit;
    private int nb_gros;
    private int nb_adulte_m;
    private int nb_adulte_f;
    private LocalDateTime dernierRepas;
    private LocalDateTime dernierBreuvage; 
    private LocalDateTime dernierLavage; 
    private LocalDateTime maladeDepuis;

    // le clapier connait son propriétaire
    @OneToOne
    @JoinColumn(name = "proprietaire", nullable = false)
    @JsonBackReference
    private Ferme proprietaire; // le propriétaire du clapier
 
    // Constructeurs
    public Clapier() {
        this.nb_bebe = 8; // Le nombre de bébés est initialisé à 8
        this.nb_petit = 0; // Le nombre de petits est initialisé à 0
        this.nb_gros = 0; // Le nombre de gros est initialisé à 0
        this.nb_adulte_m = 0; // Le nombre d'adulte males est initialisé à 0
        this.nb_adulte_f = 0; // Le nombre d'adulte femelles est initialisé à 0
        
        // Nous considérons que lors de la création du clapier, les lapins ne sont pas nourris, abreuvés et lavés
        this.dernierRepas = LocalDateTime.now().minusDays(1); // Initialisé à hier 
        this.dernierBreuvage = LocalDateTime.now().minusDays(1); // Initialisé à hier 
        this.dernierLavage = LocalDateTime.now().minusDays(1); // Initialisé à hier 
        this.maladeDepuis = null; // Le clapier n'est pas malade
    }
    // Getters et setters si nécessaire (ou utiliser @Data avec Lombok)
}
