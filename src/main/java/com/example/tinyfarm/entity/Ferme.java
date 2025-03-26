package com.example.tinyfarm.entity;
import java.time.LocalDateTime;
import java.util.List;
import java.util.ArrayList;

import com.fasterxml.jackson.annotation.JsonBackReference;
import com.fasterxml.jackson.annotation.JsonManagedReference;

import jakarta.persistence.*;
import lombok.Data;


@Entity
@Table(name = "ferme")
@Data 
public class Ferme{
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)  // Auto-incrémentation de l'ID
    private Long idFerme;

    @OneToOne(mappedBy = "idFerme") // the value of mappedBy is the name of the association-mapping attribute on the owning side
    private Compte compte; 

    @OneToOne(mappedBy = "proprietaire")
    private Remise remise;

    @OneToOne(mappedBy = "idFerme")
    private Classement classement;

    @OneToMany(mappedBy = "proprietaire")
    private List<Poule> poules;

    @OneToOne(mappedBy = "proprietaire")
    private Vache vache;

    @OneToOne(mappedBy = "proprietaire")
    private Clapier clapier;

    private String nom;
    private int ecus;
    private LocalDateTime enHibernation;
    private int achatRestant;
    private LocalDateTime dernierAchat;

    public Ferme(){}

    public Ferme(String nom){
        this.nom = nom;
        int ecus = 1500;
        Clapier clapier = new Clapier();
        Vache vache = new Vache();
        List<Poule> poules = new ArrayList<Poule>();
        poules.add(new Poule('M', 2.5, 5)); //ajout des poules a la ferme
        poules.add(new Poule('F', 2.5, 5));
        poules.add(new Poule('F', 2.5, 5));
        Remise remise = new Remise();
        Classement classement = new Classement();
        int achatRestant = 12;
    }
}